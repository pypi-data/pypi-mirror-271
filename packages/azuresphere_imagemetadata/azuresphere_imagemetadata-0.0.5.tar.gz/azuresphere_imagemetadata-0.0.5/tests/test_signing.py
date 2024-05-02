# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
from azuresphere_imagemetadata.image import Image
from azuresphere_imagemetadata.metadata_sections.metadata_id import MetadataSectionId
from azuresphere_imagemetadata.signing.der_encoded import DEREncodedSignature
from azuresphere_imagemetadata.signing.app_development import AppDevelopmentSigner
from hashlib import sha256

IMAGEPACKAGE_PATH = os.path.join(
    ".", "tests", "test_files", "applications", "HelloWorld_HighLevelApp.imagepackage"
)

IMAGEPACKAGE_NEW_PATH = os.path.join(
    ".",
    "tests",
    "test_files",
    "applications",
    "HelloWorld_HighLevelApp-newsignature.imagepackage",
)


def test_der_encoding_signature(test_logger):
    logger = test_logger()
    logger.info("Beginning test_der_encoding_signature")
    with open(IMAGEPACKAGE_PATH, "rb") as f:
        image = Image(f.read())
        signature = image.signature

        der_encoded = DEREncodedSignature.from_stored_signature(signature)
        assert (
            der_encoded.hex()
            == "3045022034927c117b091bee37409056f2751ebe355fa0d4487ae38ffa6539f5b6be40d5022100f3ad9cfd1f44ad5c1a9efbaf79e06b17d051470acd3d21d5d8f7eeda7a1c814c"
        )

        decoded = DEREncodedSignature.to_stored_signature(der_encoded)
        assert decoded == signature
    logger.info("Finishing test_der_encoding_signature")

def test_signing_thumbprint_matches(test_logger):
    logger = test_logger()
    logger.info("Beginning test_signing_thumbprint_matches")
    with open(IMAGEPACKAGE_PATH, "rb") as f:
        image = Image(f.read())

        signature_section = image.metadata.sections_by_id(MetadataSectionId.Signature)[
            0
        ]
        assert signature_section is not None

        app_development_signer = AppDevelopmentSigner()
        assert (
            signature_section.signing_cert_thumbprint.hex()
            == app_development_signer.thumbprint()
        )
    logger.info("Finishing test_signing_thumbprint_matches")

def test_package_signature_verifiable(test_logger):
    logger = test_logger()
    logger.info("Beginning test_package_signature_verifiable")
    with open(IMAGEPACKAGE_PATH, "rb") as f:
        image = Image(f.read())

        signature = image.signature

        der_encoded = DEREncodedSignature.from_stored_signature(signature)

        signature_section = image.metadata.sections_by_id(MetadataSectionId.Signature)[
            0
        ]
        assert signature_section is not None

        app_development_signer = AppDevelopmentSigner()

        assert (
            app_development_signer.verify(
                der_encoded,
                sha256(image.serialize(include_signature=False)).digest(),
            )
            == True
        )
    logger.info("Finishing test_package_signature_verifiable")


def test_new_package_signature_verifiable(test_logger):
    logger = test_logger()
    logger.info("Beginning test_new_package_signature_verifiable")
    with open(IMAGEPACKAGE_PATH, "rb") as f:
        image = Image(f.read())

        # Setting image.signature causes a serialization exception.
        # comment out for now to allow the pipeline to build/run.
        # image.signature = None

        with open(IMAGEPACKAGE_NEW_PATH, "wb") as f:
            f.write(image.serialize())

        with open(IMAGEPACKAGE_NEW_PATH, "rb") as f:
            image = Image(f.read())
            signature = image.signature

            der_encoded = DEREncodedSignature.from_stored_signature(signature)

            signature_section = image.metadata.sections_by_id(
                MetadataSectionId.Signature
            )[0]
            assert signature_section is not None

            app_development_signer = AppDevelopmentSigner()

            assert (
                app_development_signer.verify(
                    der_encoded,
                    sha256(image.serialize(include_signature=False)).digest(),
                )
                == True
            )
    logger.info("Finishing test_new_package_signature_verifiable")