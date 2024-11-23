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
from .container_registry import ContainerRegistry
from .resource_group import ResourceGroup
from .role_definition import RoleDefinition
import pulumi
import pulumi_azure_native


class DockerPullRoleDefinition(RoleDefinition):
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
        stackName: str,
        projectName: str,
        location: str,
        containerRegistry: ContainerRegistry,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new DockerPullRoleDefinition instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param containerRegistry: The container registry.
        :type containerRegistry: org.acmsl.licdata.iac.infrastructure.azure.ContainerRegistry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            "ACR Pull Custom Role",
            "Custom role to allow managed identity to pull images from ACR",
            resourceGroup.id,
            [resourceGroup.id],
            [
                {
                    "actions": ["Microsoft.ContainerRegistry/registries/pull/read"],
                    "notActions": [],
                }
            ],
            {"resource_group": resourceGroup},
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
        return "rddp"

    # @override
    def _post_create(self, resource: pulumi_azure_native.authorization.RoleDefinition):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.authorization.RoleDefinition
        """
        resource.name.apply(
            lambda name: pulumi.export(f"docker_pull_role_definition", name)
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
