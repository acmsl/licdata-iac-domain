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
from .azure_resource import AzureResource
from .container_registry import ContainerRegistry
from .resource_group import ResourceGroup
from .role_definition import RoleDefinition
from .web_app import WebApp
import pulumi
import pulumi_azure_native


class DockerPullRoleAssignment(AzureResource):
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
        stackName: str,
        projectName: str,
        location: str,
        webApp: WebApp,
        roleDefinition: RoleDefinition,
        containerRegistry: ContainerRegistry,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new DockerPullRoleAssignment instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param webApp: The WebApp.
        :type webApp: org.acmsl.licdata.iac.infrastructure.azure.WebApp
        :param roleDefinition: The role definition.
        :type roleDefinition: org.acmsl.licdata.iac.infrastructure.azure.RoleDefinition
        :param containerRegistry: The container registry.
        :type containerRegistry: org.acmsl.licdata.iac.infrastructure.azure.ContainerRegistry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "web_app": webApp,
                "role_definition": roleDefinition,
                "container_registry": containerRegistry,
                "resource_group": resourceGroup,
            },
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
        return "radp"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.authorization.RoleAssignment:
        """
        Creates a role assignment for performing docker pulls.
        :param name: The name of the role assignment.
        :type name: str
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.authorization.RoleAssignment
        """
        # the role definition id comes from `az role definition list --name AcrPull`
        return pulumi_azure_native.authorization.RoleAssignment(
            name,
            principal_id=self.web_app.identity.principal_id,
            principal_type="ServicePrincipal",
            role_definition_id=self.role_definition.id,
            scope=self.container_registry.id,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.authorization.RoleAssignment):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.authorization.RoleAssignment
        """
        resource.name.apply(
            lambda name: pulumi.export(f"docker_pull_role_assignment", name)
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
