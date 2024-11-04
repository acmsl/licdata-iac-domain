# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/functions_package.py

This script defines the FunctionsPackage class.

Copyright (C) 2024-today acmsl's licdata

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from .blob import Blob
import pulumi
import pulumi_azure_native


class FunctionsPackage(Blob):
    """
    Logic to package Licdata functions for Azure.

    Class name: FunctionsPackage

    Responsibilities:
        - Package Licdata functions for Azure.

    Collaborators:
        - None
    """

    def __init__(
        self,
        blobContainer: pulumi_azure_native.storage.BlobContainer,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new FunctionsPackage instance.
        :param blobContainer: The blob container.
        :type blobContainer: pulumi_azure_native.storage.BlobContainer
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            "rest.zip",
            pulumi.FileAsset("./rest.zip"),
            blobContainer,
            storageAccount,
            resourceGroup,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
