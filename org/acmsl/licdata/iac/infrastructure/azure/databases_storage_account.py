# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/databases_storage_account.py

This script defines the DatabasesStorageAccount class.

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
from .storage_account import StorageAccount
import pulumi
import pulumi_azure_native


class DatabasesStorageAccount(StorageAccount):
    """
    Azure Databases Storage Account for Licdata.

    Class name: DatabasesStorageAccount

    Responsibilities:
        - Define the Azure Databases Storage Account for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new StorageAccount instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__("databases", resourceGroup)
        self.storage_account.name.apply(
            lambda name: pulumi.export(f"databases_storage_account", name)
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
