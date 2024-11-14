# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/blob.py

This script defines the Blob class.

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
from pythoneda.shared import BaseObject
import pulumi
import pulumi_azure_native
from typing import List


class Blob(BaseObject):
    """
    A blob in Azure.

    Class name: Blob

    Responsibilities:
        - Declares an Azure blob.

    Collaborators:
        - None
    """

    def __init__(
        self,
        name: str,
        source: pulumi.FileAsset,
        blobContainer: pulumi_azure_native.storage.BlobContainer,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Blob instance.
        :param name: The blob name.
        :type name: str
        :param source: The source file.
        :type source: pulumi.FileAsset
        :param blobContainer: The blob container.
        :type blobContainer: pulumi_azure_native.storage.BlobContainer
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._blob = self.create_blob(
            name, source, blobContainer, storageAccount, resourceGroup
        )
        self._blob.name.apply(lambda name: pulumi.export("blob", name))

    @property
    def blob(self) -> pulumi_azure_native.storage.Blob:
        """
        Retrieves the blob.
        :return: Such blob.
        :rtype: pulumi_azure_native.storage.Blob
        """
        return self._blob

    def create_blob(
        self,
        name: str,
        source: pulumi.FileAsset,
        blobContainer: pulumi_azure_native.storage.BlobContainer,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.storage.Blob:
        """
        Creates a new Blob instance.
        :param source: The source file.
        :type source: pulumi.FileAsset
        :param blobContainer: The blob container.
        :type blobContainer: pulumi_azure_native.storage.BlobContainer
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The blob.
        :rtype: pulumi_azure_native.storage.Blob
        """
        return pulumi_azure_native.storage.Blob(
            name,
            resource_group_name=resourceGroup.name,
            account_name=storageAccount.name,
            container_name=blobContainer.name,
            type="Block",
            source=source,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._blob, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
