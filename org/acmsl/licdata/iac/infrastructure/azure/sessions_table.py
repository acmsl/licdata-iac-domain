# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/sessions_table.py

This script defines the SessionsTable class.

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
from typing import Dict, List


class SessionsTable:
    """
    Azure Sessions Table for Licdata.

    Class name: SessionsTable

    Responsibilities:
        - Define the Azure Sessions Table for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
    ):
        """
        Creates a new SessionsTable instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param storageAccount: The StorageAccount.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        """
        super().__init__()
        self._sessions_table = self.create_table(
            "sessions", storageAccount, resourceGroup
        )
        self._sessions_table.name.apply(
            lambda name: pulumi.export("sessions_table", name)
        )

    @property
    def sessions_table(self) -> pulumi_azure_native.storage.Table:
        """
        Retrieves the sessions table.
        :return: Such table.
        :rtype: pulumi_azure_native.storage.Table
        """
        return self._sessions_table

    def create_table(
        self,
        tableName: str,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.storage.Table:
        """
        Creates a new table.
        :param tableName: The name of the table.
        :type tableName: str
        :param storageAccount: The storage account.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The resource group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The table.
        :rtype: pulumi_azure_native.storage.Table
        """

        return pulumi_azure_native.storage.Table(
            tableName,
            account_name=storageAccount.name,
            table_name=tableName,
            resource_group_name=resourceGroup.name,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._sessions_table, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
