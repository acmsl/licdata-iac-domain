# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/blob.py

This script defines the Blob class.

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
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class Blob(AzureResource):
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
        stackName: str,
        projectName: str,
        location: str,
        name: str,
        blobType: str,
        source: pulumi.FileAsset,
        blobContainer: pulumi_azure_native.storage.BlobContainer,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Blob instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param name: The blob name.
        :type name: str
        :param blobType: The blob type.
        :type blobType: str
        :param source: The source file.
        :type source: pulumi.FileAsset
        :param blobContainer: The blob container.
        :type blobContainer: pulumi_azure_native.storage.BlobContainer
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "blob_container": blobContainer,
                "storage_account": storageAccount,
                "resource_group": resourceGroup,
            },
        )
        self._name = name
        self._blob_type = blobType
        self._source = source

    @property
    def name(self) -> str:
        """
        Retrieves the name.
        :return: Such name.
        :rtype: str
        """
        return self._name

    @property
    def blob_type(self) -> str:
        """
        Retrieves the type of blob.
        :return: Such information.
        :rtype: str
        """
        return self._blob_type if self._blob_type is not None else "Block"

    @property
    def source(self) -> pulumi.FileAsset:
        """
        Retrieves the blob source.
        :return: Such source.
        :rtype: pulumi.FileAsset
        """
        return self._source

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
        return "b{self.name}"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.storage.Blob:
        """
        Creates a new Blob instance.
        :param name: The name of the resource.
        :type name: str
        :return: The resource.
        :rtype: pulumi_azure_native.storage.Blob
        """
        return pulumi_azure_native.storage.Blob(
            name,
            resource_group_name=self.resource_group.name,
            account_name=self.storage_account.name,
            container_name=self.blob_container.name,
            type=self.blob_type,
            source=self.source,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.storage.Blob):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.storage.Blob
        """
        resource.name.apply(lambda name: pulumi.export("blob", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
