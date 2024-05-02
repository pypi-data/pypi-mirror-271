#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages

# read the contents of your README file
from pathlib import Path
from distutils.util import convert_path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


with open(os.path.join(this_directory, "VERSION")) as version_file:
    version = version_file.read().strip()


setup(
    name="geocover_utils",
    version=version,  # noqa: F821
    description="Set of library and tools to work with GeoCover data "
    "(https://www.swisstopo.admin.ch/en/geological-model-2d-geocover) ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="swisstopo",
    maintainer="Marc Monnerat",
    maintainer_email="marc.monnerat@swisstopo.ch",
    url="https://bitbucket.org/procrastinatio/geocover-utils",
    license="LICENSE.txt",
    packages=find_packages(where="src"),  # Automatically find packages under src
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "requests",
        "affine",
        "click",
        "geopandas",
        "gdal>=3.8.5",
        "matplotlib",
        "numpy",
        "geojson",
        "rasterio",
        "shapely >= 2.0.0",
        "pyproj",
        "pyyaml",
        "tqdm",
    ],
    tests_require=["coverage"],
    entry_points={
        "console_scripts": [
            "swissalti = geocover_utils.swissalti:download_swissalti",
        ],
    },
)
