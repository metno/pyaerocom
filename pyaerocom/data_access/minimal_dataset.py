import logging
import os

import pooch

from pyaerocom import const

logger = logging.getLogger(__name__)

#: tarfile to download
TESTDATA_FILE = "testdata-minimal.tar.gz.20231116"

minimal_dataset = pooch.create(
    path=const.OUTPUTDIR,  # ~/MyPyaerocom/
    base_url="https://pyaerocom.met.no/pyaerocom-suppl",
    registry={
        "testdata-minimal.tar.gz.20220602": "md5:5d4c6455089bc93fff1fc5e2612cf439",
        "testdata-minimal.tar.gz.20220707": "md5:86fc5cb31e8123b96ef01d44fbe93c52",
        "testdata-minimal.tar.gz.20230919": "md5:7b4c55d5258da7a2b41a3a085b947fba",
        "testdata-minimal.tar.gz.20231013": "md5:f3e311c28e341a5c54d5bbba6f9849d2",
        "testdata-minimal.tar.gz.20231017": "md5:705d91e01ca7647b4c93dfe67def661f",
        "testdata-minimal.tar.gz.20231019": "md5:f8912ee83d6749fb2a9b1eda1d664ca2",
        "testdata-minimal.tar.gz.20231116": "md5:5da747f6596817295ba7affe3402b722",
    },
)


def download_minimal_dataset(
    file_name: str = TESTDATA_FILE, /, extract_dir_override: str | None = None
):
    """Download test_data_file and extracts it.

    :param file_name : The file name to be downloaded.
    :param extract_dir : An optional folder override to where to extract the file. By
    default files are extracted into ~/MyPyaerocom
    """
    logger.debug(f"fetch {file_name} to {minimal_dataset.path}")

    if extract_dir_override is not None:
        extract_dir = os.path.abspath(extract_dir_override)
    else:
        extract_dir = "."

    minimal_dataset.path.joinpath("tmp").mkdir(parents=True, exist_ok=True)
    minimal_dataset.fetch(
        file_name, processor=pooch.Untar(["testdata-minimal"], extract_dir=extract_dir)
    )
