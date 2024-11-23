# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/app_insights.py

This script defines the AppInsights class.

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
import pulumi
import pulumi_azure_native


class AppInsights(AzureResource):
    """
    Azure Application Insights for Licdata.

    Class name: AppInsights

    Responsibilities:
        - Define the Azure Function App for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        kind: str,
        ingestionMode: str,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new AppInsights instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param kind: The type of resource.
        :type kind:
        :param ingestionMode: The ingestion mode.
        :type ingestionMode: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._kind = kind
        self._ingestion_mode = ingestionMode

    @property
    def kind(self) -> str:
        """
        Retrieves the type of App Insights.
        :return: Such type.
        :rtype: str
        """
        return self._kind if self._kind is not None else "web"

    @property
    def ingestion_mode(self) -> str:
        """
        Retrieves the ingestion mode.
        :return: Such mode.
        :rtype: str
        """
        return (
            self._ingestion_mode
            if self._ingestion_mode is not None
            else "ApplicationInsights"
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
        return "appi"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.insights.Component:
        """
        Creates an App Insights component.
        :param name: The name of the resource.
        :type name: str
        :return: The Azure App Insights component.
        :rtype: pulumi_azure_native.insights.Component
        """
        return pulumi_azure_native.insights.Component(
            name,
            resource_group_name=self.resource_group.name,
            location=self.resource_group.location,
            kind=self.kind,
            ingestion_mode=self.ingestion_mode,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.insights.Component):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.insights.Component
        """
        resource.name.apply(lambda name: pulumi.export(f"ApplicationInsights", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
