import glob
import os

import rasterio
from rasterio import merge

from geocover.logger import get_logger

logger = get_logger("geocover.raster")


def get_tiff_list(tiff_dir):
    if os.path.isdir(tiff_dir):
        return glob.glob(os.path.join(tiff_dir, "*.tif"))
    return None


def mosaic(tiff_dir, mosaic_path):
    tiff_list = get_tiff_list(tiff_dir)

    output_meta = None
    raster_to_mosaic = []
    for t in tiff_list:
        src = rasterio.open(t)
        output_meta = src.meta.copy()
        raster_to_mosaic.append(src)
        band_cnt = src.count
        for i in range(src.count):
            band = src.read(i + 1)
            logger.debug(f"{i} - {band.dtype}, {src.nodatavals}")

    # Merge
    mosaic, output = merge.merge(raster_to_mosaic)

    output_meta.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": output,
        }
    )
    logger.info(f"Writing mosaic to {mosaic_path}")
    mosaic_path_dirname = os.path.dirname(mosaic_path)
    logger.info(f"Writing mosaic to directory '{mosaic_path_dirname}'")
    if not os.path.isdir(mosaic_path_dirname):
        os.makedirs(mosaic_path_dirname)
        logger.info(f"Creating directory'{mosaic_path_dirname}'")

    with rasterio.open(mosaic_path, "w", **output_meta) as m:
        m.write(mosaic)
