# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/table.py

This script defines the Table class.

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
from org.acmsl.licdata.iac.domain import Resource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native
from typing import override


class SessionsTable(Resource):
    """
    Azure Table for Licdata.

    Class name: Table

    Responsibilities:
        - Define an Azure Table for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        name: str,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new SessionsTable instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param name: The table name.
        :type name: str
        :param storageAccount: The StorageAccount.
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
        self._name = name

    @property
    def name(self) -> str:
        """
        Returns the table name.
        :return: The table name.
        :rtype: str
        """
        return self._name

    # @override
    def _build_name(self, stackName: str, projectName: str, location: str) -> str:
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
        return f"{stackName}-{projectName}-{location}-table-{self.name}"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.storage.Table:
        """
        Creates a new table.
        :param name: The name of the resource.
        :type name: str
        :return: The table.
        :rtype: pulumi_azure_native.storage.Table
        """
        return pulumi_azure_native.storage.Table(
            name,
            account_name=self.storage_account.name,
            table_name=self.name,
            resource_group_name=self.resource_group.name,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.storage.Table):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.storage.Table
        """
        resource.name.apply(lambda name: pulumi.export("table", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
