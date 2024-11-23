# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/storage_account.py

This script defines the StorageAccount class.

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
import abc
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class StorageAccount(AzureResource, abc.ABC):
    """
    Azure Storage Account customized for Licdata.

    Class name: StorageAccount

    Responsibilities:
        - Define logic to define Azure Storage Accounts for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        name: str,
        kind: str,
        skuType: str,
        allowBlobPublicAccess: bool,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new StorageAccount instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param name: The storage account name.
        :type name: str
        :param kind: The account type.
        :type kind: str
        :param skuType: The SKU type.
        :type skuType: str
        :param allowBlobPublicAccess: Whether to allow public access to the blobs.
        :type allowBlobPublicAccess: bool
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._kind = kind
        self._sku_type = skuType
        self._allow_blob_public_access = allowBlobPublicAccess

    @property
    def kind(self) -> str:
        """
        Retrieves the account kind.
        :return: Such kind.
        :rtype: str
        """
        return self._kind if self._kind is not None else "StorageV2"

    @property
    def sku_type(self) -> str:
        """
        Retrieves the SKU type.
        :return: Such information.
        :rtype: str
        """
        return self._sku_type if self._sku_type is not None else "Standard_LRS"

    @property
    def allow_blob_public_access(self) -> bool:
        """
        Retrieves whether to allow public access to blobs.
        :return: Such condition.
        :rtype: bool
        """
        return (
            self._allow_blob_public_access
            if self._allow_blob_public_access is not None
            else True
        )

    # @override
    def _create(self, name: str) -> pulumi_azure_native.storage.StorageAccount:
        """
        Creates an Azure Storage Account.
        :param name: The name of the account.
        :type name: str
        :return: The Azure Storage Account.
        :rtype: pulumi_azure_native.storage.StorageAccount
        """
        return pulumi_azure_native.storage.StorageAccount(
            name,
            resource_group_name=self.resource_group.name,
            location=self.location,
            sku=pulumi_azure_native.storage.SkuArgs(name=self.sku_type),
            allow_blob_public_access=self.allow_blob_public_access,
            kind=self.kind,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
