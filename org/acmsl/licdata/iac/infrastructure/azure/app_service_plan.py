# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/app_service_plan.py

This script defines the AppServicePlan class.

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


class AppServicePlan(BaseObject):
    """
    Azure App Service Plan for Licdata.

    Class name: AppServicePlan

    Responsibilities:
        - Define the Azure App Service Plan for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new AppServicePlan instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._app_service_plan = self.create_app_service_plan("licenses", resourceGroup)
        self._app_service_plan.name.apply(
            lambda name: pulumi.export("app_service_plan", name)
        )

    @property
    def app_service_plan(self) -> pulumi_azure_native.web.AppServicePlan:
        """
        Retrieves the App Service Plan.
        :return: Such App Service Plan.
        :rtype: pulumi_azure_native.web.AppServicePlan
        """
        return self._app_service_plan

    def create_app_service_plan(
        self,
        appServicePlanName: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.web.AppServicePlan:
        """
        Creates an Azure App Service Plan.
        :param appServicePlanName: The name of the App Service Plan.
        :type appServicePlanName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure App Service Plan.
        :rtype: pulumi_azure_native.web.AppServicePlan
        """
        return pulumi_azure_native.web.AppServicePlan(
            appServicePlanName,
            resource_group_name=resourceGroup.name,
            kind="FunctionApp",
            # sku=pulumi_azure_native.web.SkuDescriptionArgs(tier="Dynamic", name="Y1"),
            sku=pulumi_azure_native.web.SkuDescriptionArgs(
                tier="Dynamic", name="S1", capacity=1
            ),
            location=resourceGroup.location,
            reserved=True,
            target_worker_count=1,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._app_service_plan, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
