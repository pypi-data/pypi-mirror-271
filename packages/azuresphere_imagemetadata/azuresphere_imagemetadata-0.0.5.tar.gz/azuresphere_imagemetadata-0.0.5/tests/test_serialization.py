# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
from azuresphere_imagemetadata.image import Image
from azuresphere_imagemetadata.metadata_sections.abi import (
    ABIProvidesSection,
    ABIDependsSection,
)
from azuresphere_imagemetadata.metadata_sections.compression import CompressionSection
from azuresphere_imagemetadata.metadata_sections.debug import DebugSection
from azuresphere_imagemetadata.metadata_sections.identity import IdentitySection
from azuresphere_imagemetadata.metadata_sections.image_policy import ImagePolicySection
from azuresphere_imagemetadata.metadata_sections.required_offset import (
    RequiredOffsetSection,
)
from azuresphere_imagemetadata.metadata_sections.revocation import RevocationSection
from azuresphere_imagemetadata.metadata_sections.signature import SignatureSection
from azuresphere_imagemetadata.metadata_sections.temporary_image import (
    TempImageMetadataSection,
)

IMAGEPACKAGE_PATH = os.path.join(
    ".", "tests", "test_files", "applications", "HelloWorld_HighLevelApp.imagepackage"
)


def test_deserialization(test_logger):
    logger = test_logger()
    logger.info("Beginning test_deserialization")

    with open(IMAGEPACKAGE_PATH, "rb") as f:
        image = Image(f.read())

        assert image.metadata is not None
        assert image.signature is not None
        assert image.data is not None
        assert image.metadata.signature_size == len(image.signature)

    logger.info("Finishing test_deserialization")


def test_serialization(test_logger):
    logger = test_logger()
    logger.info("Beginning test_serialization")

    with open(IMAGEPACKAGE_PATH, "rb") as f:
        data = f.read()
        image = Image(data)
        new_data = image.serialize()
        assert len(data) == len(new_data)

        for s in image.metadata.sections:
            assert s.serialize() in data

        # all data bytes should be written the same as they are read
        assert new_data == data

        assert data[: -image.metadata.signature_size] == image.serialize(
            include_signature=False
        )
    logger.info("Finishing test_serialization")

def test_section_serialization(test_logger):
    logger = test_logger()
    logger.info("Beginning test_section_serialization")
    # all sections should handle no data parameter
    # and should produce serialized data the same length as their size
    sections = [
        ABIProvidesSection(),
        ABIDependsSection(),
        CompressionSection(),
        DebugSection(),
        IdentitySection(),
        ImagePolicySection(),
        RequiredOffsetSection(),
        RevocationSection(),
        SignatureSection(),
        TempImageMetadataSection(),
    ]

    for sec in sections:
        assert sec.serialize() is not None
        assert len(sec.serialize()) == sec.size()
    logger.info("Finishing test_section_serialization")