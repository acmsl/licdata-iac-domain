# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/api.py

This script defines the Api class.

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
from .api_management_service import ApiManagementService
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class Api(AzureResource):
    """
    Azure Api for Licdata.

    Class name: Api

    Responsibilities:
        - Define the Azure Api for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        apiManagementService: ApiManagementService,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Api instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param apiManagementService: The ApiManagementService.
        :type apiManagementService: org.acmsl.licdata.iac.infrastructure.azure.ApiManagementService
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "api_management_service": apiManagementService,
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
        return "api"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.apimanagement.Api:
        """
        Creates an API.
        :param name: The name of the API.
        :type name: str
        :return: The API.
        :rtype: pulumi_azure_native.apimanagement.Api
        """
        return pulumi_azure_native.apimanagement.Api(
            name,
            resource_group_name=self.resource_group.name,
            service_name=api_management_service.name,
            path="licenses",
            protocols=["https"],
            display_name=f"{stackName}-{projectName}-{location} API",
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.apimanagement.Api):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.apimanagement.Api
        """
        resource.apply(lambda name: pulumi.export("api", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
