# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

import os, json
from shutil import rmtree
from requests import get
from zipfile import ZipFile
import pytest
from azuresphere_imagemetadata.image import ImageMetadata
from azuresphere_imagemetadata.image_manifest import ImageManifest

def clean_recovery_files_location(dest_path: str):
    if os.path.exists(dest_path):
        rmtree(dest_path)

    os.makedirs(dest_path)


def download_recovery_files(dest_path: str, recovery_url: str):
    clean_recovery_files_location(dest_path)
    response = get(recovery_url, stream=True)
    if response.status_code == 200:
        zip_file_path = os.path.join(dest_path, "recovery_images.zip")
        with open(zip_file_path, "w+b") as f:
            f.write(response.raw.read())
        with ZipFile(zip_file_path) as zf:
            zf.extractall(dest_path)
        os.remove(zip_file_path)

@pytest.mark.parametrize("osversion", ["20.01.rtm", "21.01", "22.04", "23.05"])
def test_recovery_files(test_runner, test_logger, osversion):

    RECOVERY_IMAGES_URL = f"https://staging.releases.sphere.azure.net/releaserecoveries/{osversion}.zip"
    DOWNLOAD_PATH = os.path.join(".", "tests", "test_files", "knownset_recovery_images", osversion)
    logger = test_logger()
    logger.info(f"Beginning test_recovery_files {osversion}")

    exclusions = [
        # dotnet output does not take into account daylight savings time, so timestamps will be off by an hour at certain times of the year.
        "Built On (Local)",
    ]

    download_recovery_files(DOWNLOAD_PATH, RECOVERY_IMAGES_URL)

    for file in os.listdir(DOWNLOAD_PATH):

        full_path = os.path.join(DOWNLOAD_PATH, file)

        if not os.path.isfile(full_path):
            continue

        test_runner.py_dotnet_diff_metadata(full_path, exclusions)

    logger.info("Finishing test_recovery_files")

@pytest.mark.parametrize("osversion", ["20.01.rtm", "21.01", "22.04", "23.05"])
def test_recovery_manifest_parsing(test_runner, test_logger, osversion):

    RECOVERY_IMAGES_URL = f"https://staging.releases.sphere.azure.net/releaserecoveries/{osversion}.zip"
    DOWNLOAD_PATH = os.path.join(".", "tests", "test_files", "knownset_recovery_images", osversion)
    logger = test_logger()
    logger.info(f"Beginning test_recovery_manifest_parsing {osversion}")

    download_recovery_files(DOWNLOAD_PATH, RECOVERY_IMAGES_URL)

    test_runner.py_dotnet_diff_manifest(os.path.join(DOWNLOAD_PATH, "recovery.imagemanifest"))

    logger.info("Finishing test_recovery_manifest_parsing")

@pytest.mark.parametrize("osversion", ["20.01.rtm", "21.01", "22.04", "23.05"])
def test_recovery_knownset_manifest(test_logger, osversion):
    RECOVERY_IMAGES_URL = f"https://staging.releases.sphere.azure.net/releaserecoveries/{osversion}.zip"
    DOWNLOAD_PATH = os.path.join(".", "tests", "test_files", "knownset_recovery_images", osversion)
    logger = test_logger()
    logger.info(f"Beginning test_recovery_manifest {osversion}")

    download_recovery_files(DOWNLOAD_PATH, RECOVERY_IMAGES_URL)

    with open(os.path.join(DOWNLOAD_PATH, "recovery.imagemanifest"), "rb") as f:
        byte_data = f.read()
        metadata = ImageMetadata(byte_data)

        manifest = ImageManifest.from_image_metadata(metadata)


        with open(os.path.join(".", "tests", "test_files", "knownset_recovery_manifest_metadata.json"), "r") as f:

            knownset_json =  json.loads(f.read())

            current_json = knownset_json[osversion]

            assert current_json["header"] == [manifest.header.version, manifest.header.image_count, manifest.header.manifest_header_size, manifest.header.manifest_entry_size, manifest.header.build_date]

            assert len(manifest.entries) == len(current_json["entries"])
            assert manifest.header.image_count == len(current_json["entries"])

            for entry in manifest.entries:
                assert [entry.image_uid, entry.component_uid, entry.image_type, entry.partition_type, entry.image_file_size, entry.uncompressed_image_size] in current_json["entries"]

    logger.info("Finishing test_recovery_manifest")