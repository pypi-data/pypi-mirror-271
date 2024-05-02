# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Previously called "AppTestKeyResolver" in C# code, this class is used to sign applications for development.
"""

from hashlib import sha256
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature
from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.parent


class AppDevelopmentSigner:
    """
    Uses the certificates in the ./certificates folder to sign applications for development.
    """

    def __init__(self):
        # current working theory is that tp_app_test_sign is for older image packages.
        with open(
            os.path.join(PARENT_DIR, "certificates", "tp_app_test_sign.cer"), "rb"
        ) as f:
            self.ctp_signing_cert = x509.load_pem_x509_certificate(f.read())

        # app_test_sign.pfx is for newer image packages and should be used by default.
        # code should be able to read signatures signed by either key,
        # but should only sign using app_test_sign.pfx
        with open(
            os.path.join(PARENT_DIR, "certificates", "app_test_sign.pfx"), "rb"
        ) as f:
            self.test_signing_cert = pkcs12.load_pkcs12(f.read(), None)

    def thumbprint(self):
        """
        returns the thumbprint of the "new"? app development certificate.
        """
        return self.test_signing_cert.cert.certificate.fingerprint(hashes.SHA1()).hex()

    def sign_data(self, data: bytes) -> bytes:
        """
        signs the provided data using the app development certificate
        use the "new"? certificate by default.

        returns the DER encoded signature.
        """
        return self.test_signing_cert.key.sign(
            sha256(data).digest(), ec.ECDSA(utils.Prehashed(hashes.SHA256()))
        )

    def verify(self, stored_signature: bytes, computed_hash: bytes) -> bool:
        """
        verifies the provided hash using the app development certificates.
        """
        certificates = [self.ctp_signing_cert, self.test_signing_cert.cert.certificate]

        for certificate in certificates:
            try:
                certificate.public_key().verify(
                    stored_signature,
                    computed_hash,
                    ec.ECDSA(utils.Prehashed(hashes.SHA256())),
                )
                return True
            except InvalidSignature as e:
                print(f"validation failed: {str(e)} asd")
                # if here, the signature failed to validate - continue through the list.
                pass

        return False
