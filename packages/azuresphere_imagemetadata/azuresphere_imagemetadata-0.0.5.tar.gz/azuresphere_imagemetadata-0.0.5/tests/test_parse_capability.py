# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

CAPABILITY_PATH = os.path.join(
    ".", "tests", "test_files", "capabilities", "capability_e7a13771_1.bin")


def test_capability_parser_matches(test_runner, test_logger):
    logger = test_logger()
    logger.info("Beginning test_capability_parser_matches")
    test_runner.py_dotnet_diff_metadata(CAPABILITY_PATH)
    logger.info("Finishing test_capability_parser_matches")

def test_capability_content_decodes(test_logger):
    logger = test_logger()
    logger.info("Beginning test_capability_content_decodes")
    from azuresphere_imagemetadata import image_metadata
    with open(CAPABILITY_PATH, "rb") as f:
        capability_data = f.read()
        capability_metadata = image_metadata.ImageMetadata(capability_data)

        debug_section = capability_metadata.sections_by_name("Debug")[0]

        assert debug_section is not None

        assert debug_section.image_name == "fw_config"

        from azuresphere_imagemetadata.metadata_sections.internal.capabilities import CapabilitiesSection
        capabilities_section = CapabilitiesSection(
            capability_metadata.image_data)
        assert len(capabilities_section.capabilities) > 0

        logger.info("Finishing test_capability_content_decodes")
