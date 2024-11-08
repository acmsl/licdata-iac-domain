# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/blob_container.py

This script defines the BlobContainer class.

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
import pulumi
import pulumi_azure_native
from typing import List


class BlobContainer:
    """
    A blob container in Azure.

    Class name: BlobContainer

    Responsibilities:
        - Declares an Azure blob container.

    Collaborators:
        - None
    """

    def __init__(
        self,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Blob instance.
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._blob_container = self.create_blob_container(
            "license", storageAccount, resourceGroup
        )
        self._blob_container.name.apply(
            lambda name: pulumi.export("blob_container", name)
        )

    @property
    def blob_container(self) -> pulumi_azure_native.storage.BlobContainer:
        """
        Retrieves the blob container.
        :return: Such blob container.
        :rtype: pulumi_azure_native.storage.BlobContainer
        """
        return self._blob_container

    def create_blob_container(
        self,
        name: str,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.storage.BlobContainer:
        """
        Creates a new Blob instance.
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The blob container.
        :rtype: pulumi_azure_native.storage.BlobContainer
        """
        return pulumi_azure_native.storage.BlobContainer(
            name,
            account_name=storageAccount.name,
            resource_group_name=resourceGroup.name,
            public_access="Blob",
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._blob_container, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
