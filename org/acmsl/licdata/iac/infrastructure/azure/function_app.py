# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/function_app.py

This script defines the FunctionApp class.

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
import pulumi
import pulumi_azure_native


class FunctionApp:
    """
    Azure Function App for Licdata.

    Class name: FunctionApp

    Responsibilities:
        - Define the Azure Function App for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        appServicePlan: pulumi_azure_native.web.AppServicePlan,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new FunctionApp instance.
        :param storageAccount: The StorageAccount.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param appServicePlan: The AppServicePlan.
        :type appServicePlan: pulumi_azure_native.web.AppServicePlan
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._function_app = self.create_function_app(
            "licenses", appServicePlan, storageAccount, resourceGroup
        )
        self._function_app.name.apply(lambda name: pulumi.export(f"function_app", name))
        self._function_app.default_host_name.apply(
            lambda name: pulumi.export("function_app_url", f"https://{name}")
        )

    @property
    def function_app(self) -> pulumi_azure_native.web.WebApp:
        """
        Retrieves the function web app.
        :return: Such web app.
        :rtype: pulumi_azure_native.web.WebApp
        """
        return self._function_app

    def create_function_app(
        self,
        functionName: str,
        appServicePlan: pulumi_azure_native.web.AppServicePlan,
        functionStorageAccount: pulumi_azure_native.storage.StorageAccount,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.web.WebApp:
        """
        Creates an Azure Function App.
        :param functionName: The name of the function.
        :type functionName: str
        :param appServicePlan: The App Service Plan.
        :type appServicePlan: pulumi_azure_native.web.AppServicePlan
        :param functionStorageAccount: The Storage Account.
        :type functionStorageAccount: pulumi_azure_native.storage.StorageAccount
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.web.WebApp
        """

        return pulumi_azure_native.web.WebApp(
            functionName,
            resource_group_name=resourceGroup.name,
            server_farm_id=appServicePlan.id,
            kind="FunctionApp",
            site_config=pulumi_azure_native.web.SiteConfigArgs(
                app_settings=[
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="FUNCTIONS_EXTENSION_VERSION", value="~4"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="WEBSITE_RUN_FROM_PACKAGE", value="1"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="FUNCTIONS_WORKER_RUNTIME", value="python"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="AzureWebJobsSecretStorageType", value="files"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="runtime", value="python"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="AzureWebJobsStorage__accountName",
                        value=functionStorageAccount.name,
                    ),
                ],
                linux_fx_version="Python|3.9",
            ),
            client_affinity_enabled=False,
            public_network_access="Enabled",
            location=resourceGroup.location,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._function_app, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
