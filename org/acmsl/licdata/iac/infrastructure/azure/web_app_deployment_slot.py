# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/web_app_deployment_slot.py

This script defines the WebAppDeploymentSlot class.

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
from .resource_group import ResourceGroup
from .web_app import WebApp
import pulumi
import pulumi_azure_native


class WebAppDeploymentSlot(AzureResource):
    """
    Logic to define deployment slots in Azure WebApps.

    Class name: WebAppDeploymentSlot

    Responsibilities:
        - Deployment slots for Licdata functions.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        name: str,
        filePath: str,
        webApp: WebApp,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new WebAppDeploymentSlot instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param name: The slot name.
        :type name: str
        :param filePath: The file path.
        :type filePath: str
        :param webApp: The WebApp.
        :type webApp: org.acmsl.licdata.iac.infrastructure.azure.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {"web_app": webApp, "resource_group": resourceGroup},
        )
        self._name = name
        self._file_path = filePath

    @property
    def name(self) -> str:
        """
        Retrieves the slot name.
        :return: Such name.
        :rtype: str
        """
        return self._name

    @property
    def file_path(self) -> str:
        """
        Retrieves the file path.
        :return: Such path.
        :rtype: str
        """
        return self._file_path

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
        return f"wads{self.name}"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.web.WebAppDeploymentSlot:
        """
        Creates a new WebAppDeploymentSlot instance.
        :param name: The resource name.
        :type name: str
        :return: The WebAppDeploymentSlot.
        :rtype: pulumi_azure_native.web.WebAppDeploymentSlot
        """
        return pulumi_azure_native.web.WebAppDeploymentSlot(
            name,
            name=self.name,
            resource_group_name=self.resource_group.name,
            package=pulumi.FileAsset(filePath),
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.web.WebAppDeploymentSlot):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.web.WebAppDeploymentSlot
        """
        resource.name.apply(lambda name: pulumi.export("webapp_deployment_slot", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
