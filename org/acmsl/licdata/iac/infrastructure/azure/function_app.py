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
from pythoneda.shared import BaseObject
import pulumi
import pulumi_azure_native
from pulumi_azure_native.storage import list_storage_account_keys
from pulumi import Output


class FunctionApp(BaseObject):
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
        blob: pulumi_azure_native.storage.Blob,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new FunctionApp instance.
        :param storageAccount: The StorageAccount.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param appServicePlan: The AppServicePlan.
        :type appServicePlan: pulumi_azure_native.web.AppServicePlan
        :param blob: The blob.
        :type blob: pulumi_azure_native.storage.Blob
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._function_app = self.create_function_app(
            "licenses", appServicePlan, storageAccount, blob, resourceGroup
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
        blob: pulumi_azure_native.storage.Blob,
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
        :param blob: The blob.
        :type blob: pulumi_azure_native.storage.Blob
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.web.WebApp
        """
        pkg = blob.url.apply(lambda url: url)
        storage_account_keys = list_storage_account_keys(
            resource_group_name=resourceGroup.name,
            account_name=functionStorageAccount.name,
        )
        primary_storage_key = storage_account_keys.keys[0].value
        connection_string = Output.format(
            "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net",
            functionStorageAccount.name,
            primary_storage_key,
        )
        pulumi.export("connection_string", connection_string)

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
                        name="WEBSITE_RUN_FROM_PACKAGE", value=pkg
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
                        name="AzureWebJobsStorage",
                        value=connection_string,
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="AzureWebJobsStorage__accountName",
                        value=functionStorageAccount.name.apply(lambda name: name),
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="WEBSITE_AUTH_LEVEL", value="Anonymous"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="WEBSITES_ENABLE_APP_SERVICE_STORAGE",
                        # value=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net",
                        value=False,
                    ),
                ],
                cors=pulumi_azure_native.web.CorsSettingsArgs(
                    allowed_origins=[
                        "*"
                        # "https://portal.azure.com",
                    ]
                ),
                linux_fx_version="Python|3.9",
                http20_enabled=True,
            ),
            client_affinity_enabled=False,
            public_network_access="Enabled",
            location=resourceGroup.location,
            https_only=True,
            client_cert_mode="Ignore",
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._function_app, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
