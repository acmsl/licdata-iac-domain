# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/docker_pull_role_definition.py

This script defines the DockerPullRoleDefinition class.

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


class DockerPullRoleDefinition(BaseObject):
    """
    Azure Role Definition for Licdata's Functions.

    Class name: DockerPullRoleDefinition

    Responsibilities:
        - Define the Azure Role so Licdata's Functions can perform docker pulls.

    Collaborators:
        - None
    """

    def __init__(
        self,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new DockerPullRole instance.
        :param containerRegistry: The container registry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._role_definition = self.create_role_definition(
            "docker_pull_for_licenses",
            containerRegistry,
            resourceGroup,
        )
        self._role_definition.name.apply(
            lambda name: pulumi.export(f"docker_pull_role_definition", name)
        )

    @property
    def role_definition(self) -> pulumi_azure_native.authorization.RoleDefinition:
        """
        Retrieves the role assignment.
        :return: Such instance.
        :rtype: pulumi_azure_native.authorization.Role
        """
        return self._role_definition

    def create_role_definition(
        self,
        name: str,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.authorization.RoleDefinition:
        """
        Creates a role definition for performing docker pulls.
        :param name: The name of the role.
        :type name: str
        :param containerRegistry: The containerRegistry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.authorization.RoleDefinition
        """
        return pulumi_azure_native.authorization.RoleDefinition(
            name,
            role_name="ACR Pull Custom Role",
            description="Custom role to allow managed identity to pull images from ACR",
            assignable_scopes=[resourceGroup.id],
            permissions=[
                {
                    "actions": ["Microsoft.ContainerRegistry/registries/pull/read"],
                    "notActions": [],
                }
            ],
            scope=resourceGroup.id,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._role_definition, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
