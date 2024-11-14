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
from pythoneda.shared import BaseObject
import pulumi
import pulumi_azure_native
from pulumi_azure_native.storage import list_storage_account_keys
from pulumi import Output


class AppInsights(BaseObject):
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
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new AppInsights instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._app_insights = self.create_app_insights("licenses", resourceGroup)
        self._app_insights.name.apply(lambda name: pulumi.export(f"app_insights", name))

    @property
    def app_insights(self) -> pulumi_azure_native.insights.Component:
        """
        Retrieves the app insights.
        :return: Such component.
        :rtype: pulumi_azure_native.insights.Component
        """
        return self._app_insights

    def create_app_insights(
        self,
        name: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.insights.Component:
        """
        Creates an App Insights component.
        :param name: The name of the component.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure App Insights component.
        :rtype: pulumi_azure_native.insights.Component
        """
        return pulumi_azure_native.insights.Component(
            name,
            resource_group_name=resourceGroup.name,
            location=resourceGroup.location,
            kind="web",
            ingestion_mode="ApplicationInsights",
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._app_insights, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
