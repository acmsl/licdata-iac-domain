# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/storage_account.py

This script defines the StorageAccount class.

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
import abc
import pulumi
import pulumi_azure_native


class StorageAccount(abc.ABC):
    """
    Azure Storage Account customized for Licdata.

    Class name: StorageAccount

    Responsibilities:
        - Define logic to define Azure Storage Accounts for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self, name: str, resourceGroup: pulumi_azure_native.resources.ResourceGroup
    ):
        """
        Creates a new StorageAccount instance.
        :param name: The storage account name.
        :type name: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._storage_account = self.create_storage_account(
            name, resourceGroup, "StorageV2"
        )

    @property
    def storage_account(self) -> pulumi_azure_native.storage.StorageAccount:
        """
        Retrieves the storage account.
        :return: Such storage account.
        :rtype: pulumi_azure_native.storage.StorageAccount
        """
        return self._storage_account

    def create_storage_account(
        self,
        accountName: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        kind: str,
    ) -> pulumi_azure_native.storage.StorageAccount:
        """
        Creates an Azure Storage Account.
        :param accountName: The name of the account.
        :type accountName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param kind: The kind of account.
        :type kind: str
        :return: The Azure Storage Account.
        :rtype: pulumi_azure_native.storage.StorageAccount
        """
        return pulumi_azure_native.storage.StorageAccount(
            accountName,
            resource_group_name=resourceGroup.name,
            location=resourceGroup.location,
            sku=pulumi_azure_native.storage.SkuArgs(name="Standard_LRS"),
            kind=kind,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._storage_account, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
