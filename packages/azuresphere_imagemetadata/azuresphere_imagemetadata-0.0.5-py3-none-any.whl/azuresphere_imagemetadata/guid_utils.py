# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Provides helper functions for working with Azure Sphere GUIDs.
Azure Sphere GUIDs have historically incorrectly ordered bytes.
"""


def format_guid_as_string(guid):
    """
    Formats a GUID as a string observing the same format as dotnet code.
    """
    return f"{guid[0:8]}-{guid[8:12]}-{guid[12:16]}-{guid[16:20]}-{guid[20:32]}"


def to_guid(guid_bytes: bytes):
    """
    Correctly orders a guid stored in an image package e.g. image/component uids.
    """
    guid = [0] * 16

    for i in range(0, 4):
        guid[i] = guid_bytes[3 - i]

    guid[4] = guid_bytes[5]
    guid[5] = guid_bytes[4]
    guid[6] = guid_bytes[7]
    guid[7] = guid_bytes[6]

    guid[8:] = guid_bytes[8:]

    return bytearray(guid).hex()
