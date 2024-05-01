#!/usr/bin/env python3


import json
import logging
import os
import shutil
import sys

import click
import geopandas as gpd
import matplotlib.pyplot as plt

from geocover.downloader import RemoteFileDownloader
from geocover.geometry import (
    bbox_list_to_geojson,
    build_vrt_index,
    build_vrt_overview,
    get_box,
    get_polygon,
    partition,
)
from geocover.logger import get_logger
from geocover.raster import get_tiff_list, mosaic
from geocover.stac_client import STAC

DEFAULT_DATASET = "ch.swisstopo.swissalti3d"

MIN_GRID_SIZE = 1000  # meters
MB_PER_KM2 = {"0.5": 18.0, "2.0": 1.585}

HEADERS = {"User-Agent": "ESRI ArcMap 10.8.3 TopGIS"}
DEFAULT_CFG = "swissalti.json"


def configure(ctx, param, filename):
    ctx.default_map = {}
    try:
        with open(filename, "r") as file:
            config_data = json.load(file)

            cfg = config_data.get("settings", {})
            if config_data.get("bbox"):
                cfg["bbox"] = config_data.get("bbox")
            if config_data.get("DEM"):
                if config_data.get("DEM").get("resolution"):
                    cfg["resolution"] = config_data.get("DEM").get("resolution")
                if config_data.get("DEM").get("source"):
                    cfg["mosaic_path"] = config_data.get("DEM").get("source")
            if config_data.get("log_level"):
                cfg["log_level"] = config_data.get("log_level")
            if config_data.get("geometry"):
                cfg["geometry"] = config_data.get("geometry")

        ctx.default_map = cfg
        # print(json.dumps(cfg, indent=4))

    except IOError:
        pass


def validate_coordinates(ctx, param, value):
    coordinates = None
    try:
        coordinates = json.loads(value)
    except json.decoder.JSONDecodeError:
        pass

    try:
        if coordinates is None:
            coordinates = [
                float(coord.strip()) for coord in value.replace(" ", "").split(",")
            ]
        if len(coordinates) != 4:
            raise ValueError(
                "Bounding box should have four coordinates (min_longitude, min_latitude, max_longitude, max_latitude)"
            )
        minx, miny, maxx, maxy = coordinates
        if minx > maxx or miny > maxy:
            raise ValueError(f"Bounding box {minx} > {maxx} or/and {miny} > {maxy}")

        return coordinates
    except ValueError as e:
        raise click.BadParameter(str(e), param=param)


def validate_geometry(ctx, param, value):
    coordinates = None
    if value and "Polygon" in value:
        try:
            # TODO: click is turning double quote into single one
            coordinates = json.loads(value.replace("'", '"'))
        except Exception as e:
            print(e)
    else:
        coordinates = value

    return coordinates


@click.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    default=DEFAULT_CFG,
    callback=configure,
    is_eager=True,
    expose_value=False,
    help="Read option defaults from the specified INI file",
    show_default=True,
)
@click.option(
    "-b",
    "--bbox",
    required=True,
    nargs=1,
    type=click.STRING,
    callback=validate_coordinates,
    help="Bounding box coordinates (min_longitude, min_latitude, max_longitude, max_latitude)",
)
@click.option(
    "-g",
    "--geometry",
    required=False,
    nargs=1,
    type=click.STRING,
    callback=validate_geometry,
    help="Bounding box polygon",
)
@click.option(
    "-y",
    "--yes",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Confirming the question",
)
@click.option(
    "-d",
    "--dataset",
    help="Dataset name",
    type=click.Choice([DEFAULT_DATASET], case_sensitive=True),
    default=DEFAULT_DATASET,
)
@click.option(
    "-r",
    "--resolution",
    help="DEM resolution: 0.5 or 2.0 meters (default)",
    type=click.Choice(["2.0", "0.5"], case_sensitive=False),
    default="2.0",
)
@click.option(
    "-p",
    "--proxy",
    help="Proxy to use for connection (default: None)",
    type=click.STRING,
    default=None,
)
@click.option(
    "--cache-directory",
    required=True,
    help="Directory to write the files",
    type=click.Path(dir_okay=True),
)
@click.option(
    "--cache-delete",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Delete cache before downloading",
)
@click.option(
    "-m",
    "--mosaic-path",
    required=False,
    help="Mosaic file",
    type=click.Path(dir_okay=True),
)
@click.option(
    "--progress-bar",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Display a progress bar",
)
@click.option(
    "--no-vrt",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Build a VRT for the TIFF",
)
@click.option(
    "--no-mosaic",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Build a mosaic or the TIFF",
)
@click.option(
    "-n",
    "--num-processes",
    default=4,
    help="Number of processes for parallel downloading",
)
@click.option(
    "-l",
    "--log-level",
    default="INFO",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=True
    ),
    help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def download_swissalti(*args, **kwargs):
    bbox = kwargs.get("bbox")
    geom = kwargs.get("geometry")
    dataset = kwargs.get("dataset")
    resolution = kwargs.get("resolution")
    proxy = kwargs.get("proxy")
    cache_directory = kwargs.get("cache_directory")
    num_processes = kwargs.get("num_processes")
    log_level = kwargs.get("log_level")
    yes = kwargs.get("yes")
    mosaic_path = kwargs.get("mosaic_path")
    empty_cache = kwargs.get("cache_delete")
    progress_bar = kwargs.get("progress_bar")
    no_vrt = kwargs.get("no_vrt")
    no_mosaic = kwargs.get("no_mosaic")

    logger = get_logger("geocover", level=logging.getLevelName(log_level))
    # logger.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=log_level)
    logger.debug(json.dumps(kwargs, sort_keys=True, indent=4))

    os.environ["TQDM_DISABLE"] = "1"

    for key, value in kwargs.items():
        logger.debug(f"{key}: {value}")

    stac_url = "https://data.geo.admin.ch/api/stac/v0.9"
    bounding_box = bbox
    start_datetime = "2010-01-01T00:00:00Z"
    end_datetime = ".."
    asset_type = "image/tiff; application=geotiff; profile=cloud-optimized"
    # resolution = 2.0
    updated_after = "2015-02-17T17:55:14.522904Z"
    # num_processes =
    tile_size = 1000.0

    input_extent = get_box(bbox)
    try:
        input_polygon = get_polygon(geom)
        logger.info(input_polygon)
    except AttributeError:
        input_polygon = None
    if input_polygon is not None:
        input_geometry = input_polygon
    else:
        input_geometry = input_extent

    extent_in_km2 = input_extent.area / 1000.0**2

    DOWNLOAD_SIZE = extent_in_km2 * MB_PER_KM2[resolution]

    grid = partition(input_geometry, MIN_GRID_SIZE)  # meters!
    fig, ax = plt.subplots(figsize=(15, 15))
    gpd.GeoSeries(grid).boundary.plot(ax=ax)
    gpd.GeoSeries([input_geometry]).boundary.plot(ax=ax, color="red")
    # plt.show()

    validation_msg = f"Input extent: ({extent_in_km2} km2). You will download about {DOWNLOAD_SIZE} MB for resoltion: {resolution} m. Continue? [y/n]"
    if not yes:
        if input_geometry.area >= 1:  # 3e6:
            resp = input(validation_msg)
            if resp.lower() not in ("y", "o", "yes", "oui", "ja", "j"):
                sys.exit()
    else:
        logger.info(validation_msg)

    logger.info("Starting")

    # TODO

    logger.info("Requesting the STAC server")

    stac = STAC(stac_url, proxy=proxy, progress=progress_bar)
    remote_files = stac.fetch_items(
        input_geometry,
        start_datetime,
        end_datetime,
        asset_type,
        updated_after,
        resolution,
        num_processes,
        tile_size,
    )
    logger.info("Starting to download the data files")

    tiff_dir = os.path.join(cache_directory, dataset, resolution)

    if not os.path.isdir(tiff_dir):
        os.makedirs(tiff_dir)

    if empty_cache:
        logger.info(f"Deleteing files in {tiff_dir}")
        shutil.rmtree(tiff_dir)

    headers = HEADERS
    downloader = RemoteFileDownloader(
        dataset,
        resolution,
        cache_directory,
        headers=headers,
        proxy=proxy,
        progress=progress_bar,
    )

    downloaded_files_info = downloader.download_files(bbox, remote_files, num_processes)

    boxes = [f["bbox"] for f in remote_files]
    bbox_list_to_geojson(boxes)

    for file_info in downloaded_files_info:
        if file_info is not None:
            msg = f"File: {file_info['filename']}, Size: {file_info['size']} bytes, MD5sum: {file_info['md5sum']}"
            logger.debug(msg)

    if not no_mosaic:
        mosaic(tiff_dir, mosaic_path)

    if not no_vrt:
        vrt_file_name = os.path.join(
            cache_directory, dataset, f"swissalti3d_{resolution}m.vrt"
        )

        tiff_list = get_tiff_list(tiff_dir)

        if tiff_list:
            build_vrt_index(tiff_list, vrt_file_name)
            logger.info(f"VRT file written to {vrt_file_name}")

    return 0


if __name__ == "__main__":
    download_swissalti()
