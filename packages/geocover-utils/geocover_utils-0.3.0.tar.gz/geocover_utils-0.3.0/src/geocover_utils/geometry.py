from math import ceil
import math

import numpy as np
from shapely.errors import ShapelyError
from shapely.geometry import Polygon
from shapely.prepared import prep

try:
    # Shapely version >2.0.0
    from shapely import box as shapely_box
    from shapely import union_all as shapely_union
    from shapely.geometry import shape as shapely_shape
except ImportError:
    # Shapely version 1.7
    from shapely.geometry import box as shapely_box
    from shapely.ops import unary_union as shapely_union

import json

import geojson
import shapely
from osgeo import gdal
from pyproj import Transformer


from geocover_utils.logger import get_logger

gdal.UseExceptions()

logger = get_logger("geocover.geometry")

"""
Polygon Gridding
https://www.matecdev.com/posts/shapely-polygon-gridding.html

"""


def grid_bounds(geom, delta, on_grid=False):
    """
    Return a grid covering the input geomtry

    Parameters
    ----------
    geom : shapely.geometry.Polygon
        Explanation of what a is used for within the function

    delta : float
        Size of the grid

    on_grid : boolean, optional(default=False)
        Should the grid start at origin or not

    Returns
    -------
    grid : list of shapely.geometry.Polygon
        A list of polygon coverting the input geometry


    """

    minx, miny, maxx, maxy = geom.bounds
    nx = int((maxx - minx) / delta)
    ny = int((maxy - miny) / delta)
    if on_grid:
        minx = math.floor(minx / delta) * delta
        miny = math.floor(miny / delta) * delta
        maxx = math.ceil(maxx / delta) * delta
        maxy = math.ceil(maxy / delta) * delta
        gx = np.arange(start=minx, stop=maxx + delta, step=delta)
        gy = np.arange(start=miny, stop=maxy + delta, step=delta)
    else:
        gx, gy = np.linspace(minx, maxx, nx), np.linspace(miny, maxy, ny)

    grid = []
    for i in range(len(gx) - 1):
        for j in range(len(gy) - 1):
            poly_ij = Polygon(
                [
                    [gx[i], gy[j]],
                    [gx[i], gy[j + 1]],
                    [gx[i + 1], gy[j + 1]],
                    [gx[i + 1], gy[j]],
                ]
            )
            grid.append(poly_ij)
    return grid


def partition(geom, delta, on_grid=False):
    minx, miny, maxx, maxy = geom.bounds
    if (maxx - minx) < delta or (maxy - miny) < delta:
        return [geom]
    prepared_geom = prep(geom)
    grid = list(
        filter(prepared_geom.intersects, grid_bounds(geom, delta, on_grid=on_grid))
    )
    if len(grid) < 1:
        return [geom]
    return grid


def get_box(bbox):
    return shapely_box(*bbox)


def get_polygon(geom):
    polygon = None
    try:
        polygon = shapely_shape(geom)
    except ShapelyError as e:
        logger.error(f"Polygon is not valid {geom}: {e}")
    return polygon


def bbox_list_to_geojson(boxes, fname="requested_tiles_extent.geojson", merge=True):
    geom_boxes = [shapely_box(*b) for b in boxes]
    requested_tiles_extent = None
    if merge:
        try:
            requested_tiles_extent = shapely.to_geojson(shapely_union(geom_boxes))
        except (
            OSError,
            AttributeError,
            shapely.errors.UnsupportedGEOSVersionError,
        ) as e:
            logger.error(f"Cannot convert shapely to GeoJSON: {e}")
    else:
        features = []

        for b in geom_boxes:
            # Convert Shapely box to GeoJSON Polygon
            polygon = geojson.Polygon([list(b.exterior.coords)])
            # Create GeoJSON Feature
            feature = geojson.Feature(geometry=polygon)
            features.append(feature)

        requested_tiles_extent = json.dumps(geojson.FeatureCollection(features))

    return requested_tiles_extent

    # if requested_tiles_extent:
    #    with open(f"{fname}", "w") as f:
    #        f.write(requested_tiles_extent)


def _get_transformer(srid_from, srid_to):
    return Transformer.from_crs(srid_from, srid_to, always_xy=True)


def _transform_point(coords, srid_from, srid_to):
    transformer = _get_transformer(srid_from, srid_to)
    return transformer.transform(coords[0], coords[1])


# Reprojecting pairs of coordinates and rounding them if necessary
# Only a point or a line are considered
def transform_coordinates(coordinates, srid_from, srid_to):
    if len(coordinates) % 2 != 0:
        raise ValueError
    new_coords = []
    coords_iter = iter(coordinates)
    try:
        for pnt in zip(coords_iter, coords_iter):
            new_pnt = _transform_point(pnt, srid_from, srid_to)
            new_coords += new_pnt

    except Exception as e:
        raise Exception(
            "Cannot transform coordinates {} from {} to {}: {}".format(
                coordinates, srid_from, srid_to, e
            )
        )
    return new_coords


def split_boxes(bbox, tile_size=5000):
    MINX, MINY, MAXX, MAXY = bbox
    width, height = MAXX - MINX, MAXY - MINY

    if width < tile_size and height < tile_size:
        return [bbox]

    # input_extent = shapely_box(MINX, MINY, MAXX, MAXY)

    rangex = ceil(width / tile_size)
    rangey = ceil(height / tile_size)

    stepx = width / rangex
    stepy = height / rangey
    logger.debug(f"width={width}, height={height}")
    logger.debug(f"stepx={stepx}, stepy={stepy}")

    boxes = []

    for i in range(rangex):
        for j in range(rangey):
            minx = MINX + i * stepx
            maxx = MINX + (i + 1) * stepx
            miny = MINY + j * stepy
            maxy = MINY + (j + 1) * stepy
            boxes.append((minx, miny, maxx, maxy))

    return boxes


def build_vrt_index(tiff_list, vrt_file_name):
    try:
        vrt_options = gdal.BuildVRTOptions(resampleAlg="cubic", addAlpha=True)
        gdal.BuildVRT(vrt_file_name, tiff_list, options=vrt_options)
    except (OSError, RuntimeError) as e:
        logger.error(f"Cannot build VRT index: {e}")


def build_vrt_overview(vrt_file_name):
    try:
        raster = gdal.OpenEx(vrt_file_name, gdal.OF_READONLY)
        gdal.SetConfigOption("COMPRESS_OVERVIEW", "DEFLATE")
        raster.BuildOverviews("AVERAGE", [2, 4, 8, 16, 32, 64, 128, 256])
    except (OSError, RuntimeError) as e:
        logger.error(f"Cannot build VRT overviews: {e}")
