# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/docker_pull_role_assignment.py

This script defines the DockerPullRoleAssignment class.

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


class DockerPullRoleAssignment(BaseObject):
    """
    Azure Role Assignment for Licdata's Functions.

    Class name: DockerPullRoleAssignment

    Responsibilities:
        - Define the Azure Role Assignment so Licdata's Functions can perform docker pulls.

    Collaborators:
        - None
    """

    def __init__(
        self,
        functionApp: pulumi_azure_native.web.WebApp,
        roleDefinition: pulumi_azure_native.authorization.RoleDefinition,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new DockerPullRoleAssignment instance.
        :param functionApp: The Function App.
        :type functionApp: pulumi_azure_native.web.WebApp
        :param roleDefinition: The role definition.
        :type roleDefinition: pulumi_azure_native.authorization.RoleDefinition
        :param containerRegistry: The container registry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._role_assignment = self.create_role_assignment(
            "docker_pull_for_licenses_assignment",
            functionApp,
            roleDefinition,
            containerRegistry,
            resourceGroup,
        )
        self._role_assignment.name.apply(
            lambda name: pulumi.export(f"docker_pull_role_assignment", name)
        )

    @property
    def role_assignment(self) -> pulumi_azure_native.authorization.RoleAssignment:
        """
        Retrieves the role assignment.
        :return: Such instance.
        :rtype: pulumi_azure_native.authorization.RoleAssignment
        """
        return self._role_assignment

    def create_role_assignment(
        self,
        name: str,
        functionApp: pulumi_azure_native.web.WebApp,
        roleDefinition: pulumi_azure_native.authorization.RoleDefinition,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.authorization.RoleAssignment:
        """
        Creates a role assignment for performing docker pulls.
        :param name: The name of the role assignment.
        :type name: str
        :param functionApp: The Function App.
        :type functionApp: pulumi_azure_native.web.WebApp
        :param roleDefinition: The role definition.
        :type roleDefinition: pulumi_azure_native.authorization.RoleDefinition
        :param containerRegistry: The containerRegistry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.authorization.RoleAssignment
        """
        # the role definition id comes from `az role definition list --name AcrPull`
        return pulumi_azure_native.authorization.RoleAssignment(
            name,
            principal_id=functionApp.identity.principal_id,
            principal_type="ServicePrincipal",
            role_definition_id=roleDefinition.id,
            scope=containerRegistry.id,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._role_assignment, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
