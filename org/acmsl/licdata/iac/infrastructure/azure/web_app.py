# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/web_app.py

This script defines the WebApp class.

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
from org.acmsl.licdata.iac.domain import Resource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native
from pulumi_azure_native.storage import list_storage_account_keys
from pulumi import Output
from typing import override


class WebApp(Resource):
    """
    Azure Web App for Licdata.

    Class name: WebApp

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
        appInsights: org.acmsl.licdata.iac.infrastructure.azure.AppInsights,
        storageAccount: org.acmsl.licdata.iac.infrastructure.azure.StorageAccount,
        appServicePlan: org.acmsl.licdata.iac.infrastructure.azure.AppServicePlan,
        containerRegistry: org.acmsl.licdata.iac.infrastructure.azure.ContainerRegistry,
        resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup,
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
        :type appInsights: org.acmsl.licdata.iac.infrastructure.azure.AppInsights
        :param storageAccount: The StorageAccount.
        :type storageAccount: org.acmsl.licdata.iac.infrastructure.azure.StorageAccount
        :param appServicePlan: The AppServicePlan.
        :type appServicePlan: org.acmsl.licdata.iac.infrastructure.azure.AppServicePlan
        :param containerRegistry: The container registry.
        :type containerRegistry: org.acmsl.licdata.iac.infrastructure.azure.ContainerRegistry
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "app_insights": appInsights,
                "storage_account": storageAccount,
                "container_registry": containerRegistry,
                "resource_group": resourceGroup,
            },
        )

    # @override
    def _build_name(self, stackName: str, projectName: str, location: str) -> str:
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
        return f"{stackName}-{projectName}-{location}-web-app"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.web.WebApp:
        """
        Creates an Azure Function App.
        :param name: The name of the app.
        :type name: str
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
                resource_group_name=self.resource_group.name,
                registry_name=self.container_registry.name,
            )
        )

        acr_username = acr_credentials.username
        acr_password = acr_credentials.passwords[0].value

        storage_account_keys = list_storage_account_keys(
            resource_group_name=self.resource_group.name,
            account_name=self.storage_account.name,
        )
        primary_storage_key = storage_account_keys.keys[0].value
        connection_string = Output.format(
            "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net",
            self.storage_account.name,
            primary_storage_key,
        )
        pulumi.export("connection_string", connection_string)

        return pulumi_azure_native.web.WebApp(
            name,
            resource_group_name=self.resource_group.name,
            server_farm_id=self.app_service_plan.id,
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
                        value=self.storage_account.name.apply(lambda name: name),
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
                        value=self.app_insights.instrumentation_key,
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="APPLICATIONINSIGHTS_CONNECTION_STRING",
                        value=self.app_insights.connection_string,
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
                        value=self.container_registry.admin_user_enabled.apply(
                            lambda enabled: acr_username if enabled else ""
                        ),
                    ),
                    pulumi_azure_native.web.NameValuePairArgs(
                        name="DOCKER_REGISTRY_SERVER_PASSWORD",
                        value=self.container_registry.admin_user_enabled.apply(
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
            location=self.location,
            https_only=True,
            client_cert_mode="Ignore",
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.web.WebApp):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.web.WebApp
        """
        resource.name.apply(lambda name: pulumi.export(f"function_app", name))
        resource.default_host_name.apply(
            lambda name: pulumi.export("function_app_url", f"https://{name}")
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
