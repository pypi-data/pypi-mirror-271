# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

from .image_metadata import ImageMetadata
from .signing.app_development import AppDevelopmentSigner
from .signing.der_encoded import DEREncodedSignature


class Image:
    def __init__(self, data=None):
        self.signature = None
        self.data = data
        self.metadata = ImageMetadata(None)
        if data is not None:
            self.deserialize(data)

    def as_bytes(self, signer=AppDevelopmentSigner(), include_signature=False):
        new_data = self.data + self.metadata.serialize()
        if include_signature:
            if self.signature is None:
                self.signature = DEREncodedSignature.to_stored_signature(
                    signer.sign_data(new_data)
                )
            return new_data + self.signature
        return new_data

    def deserialize(self, data):
        try:
            self.metadata = ImageMetadata(data)
        except Exception as e:
            print(f"Metadata parsing failed: {e}")
            # metadata parsing could not correctly find the metadata
            return

        self.data = data[: self.metadata.start_of_metadata]
        self.signature = data[self.metadata.end_of_metadata :]

        if len(self.signature) != self.metadata.signature_size:
            raise Exception("Signature size mismatch")

    def serialize(self, signer=AppDevelopmentSigner(), include_signature=True):
        return self.as_bytes(signer, include_signature)
