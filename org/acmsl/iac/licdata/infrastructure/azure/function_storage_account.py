# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/function_storage_account.py

This script defines the FunctionStorageAccount class.

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
from .resource_group import ResourceGroup
from .storage_account import StorageAccount
import pulumi
import pulumi_azure_native


class FunctionStorageAccount(StorageAccount):
    """
    Azure Function Storage Account for Licdata.

    Class name: FunctionStorageAccount

    Responsibilities:
        - Define the Azure Function Storage Account for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new FunctionStorageAccount instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            None,
            None,
            None,
            None,
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
        return "saf"

    # @override
    def _post_create(self, resource: pulumi_azure_native.storage.StorageAccount):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.storage.StorageAccount
        """
        resource.name.apply(
            lambda name: pulumi.export(f"function_storage_account", name)
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
