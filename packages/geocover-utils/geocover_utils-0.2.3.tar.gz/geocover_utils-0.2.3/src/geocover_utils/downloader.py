import os
import signal
import sys
from hashlib import md5
from multiprocessing import Pool

import requests
from tqdm import tqdm

from geocover.geometry import transform_coordinates

from geocover.logger import get_logger

logger = get_logger("geocover.download")

STAC_SERVICE_URL = "https://data.geo.admin.ch/api/stac/v0.9/collections"

TIMEOUT = 30


def init_pool():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class RemoteFileDownloader:
    def __init__(
        self,
        dataset,
        resolution,
        cache_directory,
        proxy=None,
        headers={},
        progress=True,
    ):
        self.dataset = dataset
        self.resolution = resolution
        self.cache_directory = os.path.join(cache_directory, dataset, str(resolution))
        self.proxy = {"https": proxy} if proxy is not None else proxy
        # self.logger = get_logger(__name__)
        self.headers = headers
        self.progress = progress

        os.makedirs(self.cache_directory, exist_ok=True)

    def _flush_logger(self):
        logger.handlers[0].flush()

    def _calculate_md5(self, data):
        return md5(data).hexdigest()

    def _get_cache_path(self, filename):
        return os.path.join(self.cache_directory, filename)

    def _download_file(self, args):
        url, filename = args
        # cache_path = self._get_cache_path(filename)

        if os.path.exists(filename):
            logger.debug(
                f"File {filename} already exists in the cache. Skipping download."
            )

            return None

        response = requests.get(
            url, proxies=self.proxy, headers=self.headers, timeout=TIMEOUT
        )
        if response.status_code == 200:
            # cache_path = self._get_cache_path(filename)
            with open(filename, "wb") as file:
                file.write(response.content)
            return {
                "filename": filename,
                "size": len(response.content),
                "md5sum": self._calculate_md5(response.content),
            }

    def _get_remote_files(self, bounding_box):
        # Your logic to get a list of file names based on the bounding box
        # For example, construct query parameters and append to base URL
        url = f"{STAC_SERVICE_URL}/{self.dataset}/items"

        bbox = ",".join(map(str, transform_coordinates(bounding_box, 2056, 4326)))

        response = requests.get(
            url, params={"bbox": bbox}, proxies=self.proxy, timeout=TIMEOUT
        )

        if response.status_code == 200:
            return (
                response.json()
            )  # Assuming the server returns a JSON list of file names

    def _process_chunk(self, args):
        item = self._download_file(args)

        return item

    def download_files(self, bounding_box, remote_files, num_processes=4):
        # remote_files = self._get_remote_files(bounding_box)

        if not remote_files:
            logger.error("No files found.")
            return []

        # No reason to create the pool over and over again:
        with Pool(initializer=init_pool, processes=num_processes) as pool:
            try:
                download_args = [
                    (f.get("href"), os.path.join(self.cache_directory, f.get("id")))
                    for f in remote_files
                ]

                # Use tqdm for progress tracking
                with tqdm(
                    total=len(download_args),
                    desc="Fetching files",
                    disable=not self.progress,
                ) as pbar:

                    def update_progress(*_):
                        pbar.update()
                        sys.stdout.flush()

                    try:
                        items = []
                        for chunk_items in pool.imap_unordered(
                            self._process_chunk, download_args
                        ):
                            # items.extend(chunk_items)
                            items.append(chunk_items)
                            update_progress()

                    finally:
                        pbar.close()
                        pool.close()
                        pool.join()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt: Stopping the processes...")
                pbar.close()
                pool.terminate()
                pool.join()
                sys.exit(3)

        downloaded_files_info = items

        not_downloaded_files = sum(f is None for f in downloaded_files_info)
        total_files_number = len(downloaded_files_info)

        logger.info(
            f"Files processed: {total_files_number}. Downloaded: {total_files_number - not_downloaded_files}"
        )

        # self._flush_logger()
        return downloaded_files_info
