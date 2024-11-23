# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/licdata_web_app.py

This script defines the LicdataWebApp class.

Copyright (C) 2024-today acmsl's IaC

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
from .app_insights import AppInsights
from .app_service_plan import AppServicePlan
from .container_registry import ContainerRegistry
from .resource_group import ResourceGroup
from .storage_account import StorageAccount
import pulumi
import pulumi_azure_native
from pulumi_azure_native.storage import list_storage_account_keys
from pulumi import Output


class LicdataWebApp(WebApp):
    """
    Azure Web App for Licdata.

    Class name: LicdataWebApp

    Responsibilities:
        - Define the Azure Web App for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        appInsights: AppInsights,
        storageAccount: StorageAccount,
        appServicePlan: AppServicePlan,
        containerRegistry: ContainerRegistry,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new WebApp instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param appInsights: The App Insights instance.
        :type appInsights: pythoneda.iac.pulumi.azure.AppInsights
        :param storageAccount: The StorageAccount.
        :type storageAccount: pythoneda.iac.pulumi.azure.StorageAccount
        :param appServicePlan: The AppServicePlan.
        :type appServicePlan: pythoneda.iac.pulumi.azure.AppServicePlan
        :param containerRegistry: The container registry.
        :type containerRegistry: pythoneda.iac.pulumi.azure.ContainerRegistry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pythoneda.iac.pulumi.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            "licdata",
            "latest",
            "licenses.azurecr.io",  # containerRegistry.login_server.apply(lambda name: name)
            {
                "app_insights": appInsights,
                "storage_account": storageAccount,
                "app_service_plan": appServicePlan,
                "container_registry": containerRegistry,
                "resource_group": resourceGroup,
            },
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
