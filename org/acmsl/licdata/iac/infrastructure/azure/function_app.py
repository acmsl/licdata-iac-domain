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
        appInsights: pulumi_azure_native.insights.Component,
        storageAccount: pulumi_azure_native.storage.StorageAccount,
        appServicePlan: pulumi_azure_native.web.AppServicePlan,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new FunctionApp instance.
        :param appInsights: The App Insights instance.
        :type appInsights: pulumi_azure_native.insights.Component
        :param storageAccount: The StorageAccount.
        :type storageAccount: pulumi_azure_native.storage.StorageAccount
        :param appServicePlan: The AppServicePlan.
        :type appServicePlan: pulumi_azure_native.web.AppServicePlan
        :param containerRegistry: The container registry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._function_app = self.create_function_app(
            "licenses",
            appInsights,
            appServicePlan,
            storageAccount,
            containerRegistry,
            resourceGroup,
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
        appInsights: pulumi_azure_native.insights.Component,
        appServicePlan: pulumi_azure_native.web.AppServicePlan,
        functionStorageAccount: pulumi_azure_native.storage.StorageAccount,
        containerRegistry: pulumi_azure_native.containerregistry.Registry,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.web.WebApp:
        """
        Creates an Azure Function App.
        :param functionName: The name of the function.
        :type functionName: str
        :param appInsights: The App Insights instance.
        :type appInsights: pulumi_azure_native.insights.Component
        :param appServicePlan: The App Service Plan.
        :type appServicePlan: pulumi_azure_native.web.AppServicePlan
        :param functionStorageAccount: The Storage Account.
        :type functionStorageAccount: pulumi_azure_native.storage.StorageAccount
        :param containerRegistry: The containerRegistry.
        :type containerRegistry: pulumi_azure_native.containerregistry.Registry
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.web.WebApp
        """
        # login_server = containerRegistry.login_server.apply(lambda name: name)
        login_server = "licenses.azurecr.io"
        image_url = f"{login_server}/licdata:latest"
        # login_server = containerRegistry.name.apply(
        #    lambda name: f"{name}.azurecr.io/licdata:latest"
        # )
        # self.__class__.logger().info(f"login_server: {login_server}")

        # pulumi.Output.concat(
        #    containerRegistry.login_server, "/licdata:latest"
        # )
        acr_credentials = (
            pulumi_azure_native.containerregistry.list_registry_credentials(
                resource_group_name=resourceGroup.name,
                registry_name=containerRegistry.name,
            )
        )

        acr_username = acr_credentials.username
        acr_password = acr_credentials.passwords[0].value

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
            kind="FunctionApp,linux,container",
            identity=pulumi_azure_native.web.ManagedServiceIdentityArgs(
                type="SystemAssigned"
            ),
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
                        value=False,
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="APPINSIGHTS_INSTRUMENTATIONKEY",
                        value=appInsights.instrumentation_key,
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="APPLICATIONINSIGHTS_CONNECTION_STRING",
                        value=appInsights.connection_string,
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="LD_LIBRARY_PATH", value="/home/site/wwwroot"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="FUNCTIONS_WORKER_PROCESS_COUNT", value="1"
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="DOCKER_REGISTRY_SERVER_URL",
                        value=f"https://{login_server}",
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="DOCKER_REGISTRY_SERVER_USERNAME",
                        value=containerRegistry.admin_user_enabled.apply(
                            lambda enabled: acr_username if enabled else ""
                        ),
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="DOCKER_REGISTRY_SERVER_PASSWORD",
                        value=containerRegistry.admin_user_enabled.apply(
                            lambda enabled: (acr_password if enabled else "")
                        ),
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="WEBSITES_PORT", value="80"
                    ),
                ],
                cors=pulumi_azure_native.web.CorsSettingsArgs(allowed_origins=["*"]),
                linux_fx_version=f"DOCKER|{image_url}",
                http_logging_enabled=True,
                http20_enabled=True,
                ftps_state="AllAllowed",
                scm_type="LocalGit",
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
        try:
            return getattr(self._function_app, attr)
        except AttributeError as e:
            raise AttributeError(
                f"'{type(self._function_app).__name__}' object has no attribute '{attr}"
            )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
