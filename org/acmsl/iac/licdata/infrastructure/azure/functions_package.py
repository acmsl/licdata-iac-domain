# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/functions_package.py

This script defines the FunctionsPackage class.

Copyright (C) 2024-today acmsl's Licdata IaC

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
from .blob_container import BlobContainer
from .storage_account import StorageAccount
from .resource_group import ResourceGroup
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
        blobContainer: BlobContainer,
        storageAccount: StorageAccount,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new FunctionsPackage instance.
        :param blobContainer: The blob container.
        :type blobContainer: org.acmsl.iac.licdata.infrastructure.azure.BlobContainer
        :param storageAccount: The storage account.
        :type storageAccount: org.acmsl.iac.licdata.infrastructure.azure.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            "rest.zip",
            pulumi.FileAsset("./rest.zip"),
            blobContainer,
            storageAccount,
            resourceGroup,
        )

    # @override
    def _resource_name(self, stackName: str, projectName: str, location: str) -> str:
        """
        Builds the resource name.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :return: The resource name.
        :rtype: str
        """
        return "bfp"


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
