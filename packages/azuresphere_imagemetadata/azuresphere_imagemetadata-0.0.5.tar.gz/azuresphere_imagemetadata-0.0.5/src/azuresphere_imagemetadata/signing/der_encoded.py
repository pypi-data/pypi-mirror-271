# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Takes a signature stored in the image and converts it to DER encoded format for use with pyca/cryptography.
C# code simply appends the R/S consecutively in byte format for the signature. This is not DER encoded.
"""

import struct


class DEREncodedSignature:
    @staticmethod
    def from_stored_signature(stored_signature: bytes) -> bytes:
        """
        Converts a stored signature to DER encoded format.
        """
        # C#/dotnet does not output a DER encoded signature, so we need to convert it.
        # der encoded signature is generally:
        # 0x30, payload length, 0x20, r length, r, 0x20, s length, s
        # for compatibility with dotnet, r length and s length must be 32 bytes long
        # if the first byte of r/s is >= 0x80, then 0 is added to the front of the r/s.
        # if the first byte of r/s is 0x00, then it is removed.
        # This is the only format supported.
        if len(stored_signature) != 64:
            raise Exception("Invalid stored signature length")
        r = stored_signature[:32]
        s = stored_signature[32:]

        to_encode = [r, s]
        der_encoded = bytearray([0x30])

        encoded_buf = bytearray()
        for sig in to_encode:
            if sig[0] >= 0x80:
                encoded_buf.extend(bytearray([0x02, len(sig) + 1, 0]))
            else:
                encoded_buf.extend(bytearray([0x02, len(sig)]))
            encoded_buf.extend(sig)

        der_encoded.extend([len(encoded_buf)])
        der_encoded.extend(encoded_buf)
        return bytes(der_encoded)

    @staticmethod
    def to_stored_signature(der_encoded_signature: bytes) -> bytes:
        """
        Converts a DER encoded signature to the format used by the Azure Sphere SDK.
        This code does not support all DER encoded signatures, only the format used by the Azure Sphere SDK.
        """
        # der encoded signature is generally:
        # 0x30, payload length, 0x20, r length, r, 0x20, s length, s
        # for compatibility with dotnet, r length and s length must be 32 bytes long
        # if the first byte of r/s is >= 0x80, then 0 is added to the front of the r/s.
        # if the first byte of r/s is 0x00, then it is removed

        # extract the DER signature header
        der_type, payload_length = struct.unpack_from("BB", der_encoded_signature)
        if der_type != 0x30:
            raise Exception("Invalid DER encoded signature. Incorrect type.")

        if payload_length != len(der_encoded_signature) - 2:
            raise Exception("Invalid DER encoded signature. Incorrect payload length.")

        remainder = der_encoded_signature[2:]
        signature_values = []  # r/s value storage
        while remainder != bytearray():
            (var_type, sig_length) = struct.unpack_from("BB", remainder)
            remainder = remainder[2:]  # consume the type and length info.
            # validate type as integer
            if var_type != 0x02:
                raise Exception("Invalid DER encoded signature")
            # ensure length is 32 bytes or 33 bytes (if first byte is 0x00)
            if sig_length not in [0x20, 0x21]:
                raise Exception("Invalid DER encoded signature")

            if sig_length == 0x21:
                if remainder[0] != 0x00:
                    raise Exception("Invalid DER encoded signature")
                # consume the byte
                remainder = remainder[1:]
            # stored the signature value
            signature_values.append(remainder[:sig_length])
            remainder = remainder[sig_length:]

        ## return r combined with s
        return signature_values[0] + signature_values[1]
