
import os
from pathlib import Path
import rasterio

this_directory = Path(__file__).parent

with open(os.path.join(this_directory,'..',  "VERSION")) as version_file:
    version = version_file.read().strip()

def test_swissalti_version(script_runner):
    result = script_runner.run(['swissalti', '--version'])
    assert result.returncode == 0
    assert result.stdout == f'swissalti, version {version}\n'
    assert result.stderr == ''

def test_swissalti_with_config(script_runner):
    result = script_runner.run(['swissalti', '--config', 'tests/test_config.json', '--yes', '--log-level', 'CRITICAL'])
    assert result.returncode == 0
    assert result.stderr == ''

    with  rasterio.open('./test/swissalti3d-2.0-mosaic.tif') as dataset:
        left, bottom, right, top = dataset.bounds
        assert top == 1168000.0
        assert left == 2587000
        assert bottom == 1165000.0
        assert right == 2594000.0
