# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/blob_container.py

This script defines the BlobContainer class.

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
from .storage_account import StorageAccount
import pulumi
import pulumi_azure_native
from typing import Any


class BlobContainer(AzureResource):
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
        stackName: str,
        projectName: str,
        location: str,
        publicAccess: str,
        storageAccount: StorageAccount,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Blob Container instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param publicAccess: The public access type.
        :type publicAccess
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {"storage_account": storageAccount, "resource_group": resourceGroup},
        )
        self._public_access = publicAccess

    @property
    def public_access(self) -> str:
        """
        Retrieves the public access value.
        :return: Such information.
        :rtype: str
        """
        return self._public_access if self._public_access is not None else "Blob"

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
        return "bc"

    # @override
    def _create(self, name: str) -> Any:
        """
        Creates a new Blob Container instance.
        :param name: The name of the resource.
        :type name: str
        :return: The blob container.
        :rtype: pulumi_azure_native.storage.BlobContainer
        """
        return pulumi_azure_native.storage.BlobContainer(
            name,
            account_name=self.storage_account.name,
            resource_group_name=self.resource_group.name,
            public_access=self.public_access,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.storage.BlobContainer):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.storage.BlobContainer
        """
        resource.name.apply(lambda name: pulumi.export("blob_container", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
