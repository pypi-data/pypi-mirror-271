from multiprocessing import Pool

import geopandas as gpd
import requests
from shapely import box as shapely_box
from tqdm import tqdm

from geocover.geometry import (
    bbox_list_to_geojson,
    partition,
    split_boxes,
    transform_coordinates,
)
from geocover.logger import get_logger

logger = get_logger("geocover.stac")


class STAC:
    def __init__(self, stac_url, proxy=None, progress=True):
        self.stac_url = stac_url
        self.proxy = {"https": proxy} if proxy is not None else proxy
        self.progress = progress

    def _fetch_items(self, params):
        try:
            response = requests.get(
                self.stac_url + "/collections/ch.swisstopo.swissalti3d/items",
                params=params,
                proxies=self.proxy,
            )

            response.raise_for_status()
            return response.json().get("features", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching items: {e}")
            return []

    def _filter_items(self, items, asset_type=None, updated_after=None):
        filtered_items = []

        for item in items:
            properties = item.get("properties", {})
            assets = item.get("assets", {})

            # Apply filtering based on asset properties
            if asset_type is None or (assets and asset_type in assets.values()):
                if updated_after is None or (
                    properties.get("updated") and properties["updated"] > updated_after
                ):
                    filtered_items.append(item)

        return filtered_items

    def _filter_asset(
        self, asset, asset_type=None, resolution=None, updated_after=None
    ):
        # Apply filtering based on asset properties
        if asset_type is None or (asset and asset_type in asset.values()):
            # print('type', asset.get('eo:gsd'))
            if resolution is None or (resolution in str(asset.get("eo:gsd"))):
                return True

        return False

    def _filter_features(
        self, results, asset_type=None, resolution=None, updated_after=None
    ):
        filtered_items = []

        for feature in results:
            """
            for features in results:
            for feature in features:
            """
            logger.debug(feature)
            feature_properties = feature.get("properties", {})
            feature_bbox = feature.get("bbox", {})

            if updated_after is None or (
                feature_properties.get("updated")
                and feature_properties["updated"] > updated_after
            ):
                assets = feature.get("assets", [])

                for asset_key in assets.keys():
                    asset = assets[asset_key]

                    if self._filter_asset(asset, asset_type, resolution, updated_after):
                        asset["id"] = asset_key
                        asset["bbox"] = feature_bbox
                        filtered_items.append(asset)

        return filtered_items

    def _process_chunk(self, params):
        items = self._fetch_items(params)

        return items

    def fetch_items(
        self,
        bounding_box,
        start_datetime=None,
        end_datetime=None,
        asset_type=None,
        updated_after=None,
        resolution="2.0",
        num_processes=4,
        tile_size=1000,
    ):
        pool = Pool(processes=num_processes)
        # chunk_size = 10  # You may adjust the chunk size based on your needs

        if isinstance(resolution, (int, float)):
            resolution = f"{resolution:.1f}"

        # shapely geom
        tiles = partition(bounding_box, tile_size)  # met

        logger.debug(bounding_box)
        logger.debug(tile_size)
        logger.debug(tiles)

        params = {
            # "bbox": bounding_box,
            "datetime": f"{start_datetime}/{end_datetime}"
            if start_datetime and end_datetime
            else None,
        }

        boxes = tiles

        gdf = gpd.GeoSeries(tiles).boundary
        # gdf.to_file("tiles_lv95.geojson", driver="GeoJSON")

        # bbox_list_to_geojson(boxes, fname="tiles_lv95.geojson", merge=False)

        params_list = []
        for tile in tiles:
            p = params.copy()
            t = tile.bounds
            p["bbox"] = ",".join(map(str, transform_coordinates(t, 2056, 4326)))
            params_list.append(p)

        boxes = [list(map(float, b["bbox"].split(","))) for b in params_list]
        bbox_list_to_geojson(boxes, fname="tiles_wgs84.geojson")

        # Use tqdm for progress tracking
        with tqdm(
            total=len(params_list),
            desc="Getting STAC metadata items",
            disable=not self.progress,
        ) as pbar:

            def update_progress(*_):
                pbar.update()

            try:
                items = []
                for chunk_items in pool.imap_unordered(
                    self._process_chunk, params_list
                ):
                    items.extend(chunk_items)
                    update_progress()

            finally:
                pbar.close()
                pool.close()
                pool.join()

        results = items

        filtered_items = []

        filtered_items = self._filter_features(
            results, asset_type, resolution, updated_after
        )

        return filtered_items


if __name__ == "__main__":
    # Example usage
    stac_url = "https://data.geo.admin.ch/api/stac/v0.9"
    bounding_box = (2600000, 1200000, 2611000, 1207000)  # (7.4,46,7.5,46.5)
    start_datetime = "2010-01-01T00:00:00Z"
    end_datetime = ".."
    asset_type = "image/tiff; application=geotiff; profile=cloud-optimized"
    resolution = "2.0"
    updated_after = "2015-02-17T17:55:14.522904Z"
    num_processes = 4

    tile_size = 5 * 1000.0

    stac = STAC(stac_url, progress=False)
    items = stac.fetch_items(
        shapely_box(*bounding_box),
        start_datetime,
        end_datetime,
        asset_type,
        updated_after,
        resolution,
        num_processes,
        tile_size,
    )

    logger.info(f"Fetched {len(items)} items.")
