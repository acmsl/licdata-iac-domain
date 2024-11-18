# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/pulumi_azure_stack.py

This script defines the PulumiAzureStack class.

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
from org.acmsl.licdata.iac.infrastructure import PulumiStack
from .resource_group import ResourceGroup
from .function_storage_account import FunctionStorageAccount
from .app_service_plan import AppServicePlan
from .web_app import WebApp
from .public_ip_address import PublicIpAddress
from .dns_zone import DnsZone
from .dns_record import DnsRecord
from .blob_container import BlobContainer
from .functions_package import FunctionsPackage
from .functions_deployment_slot import FunctionsDeploymentSlot
from .app_insights import AppInsights
from .container_registry import ContainerRegistry
from .docker_pull_role_definition import DockerPullRoleDefinition
from .docker_pull_role_assignment import DockerPullRoleAssignment


class PulumiAzureStack(PulumiStack):
    """
    Azure-specific Pulumi implementation of Licdata infrastructure stacks.

    Class name: PulumiAzureStack

    Responsibilities:
        - Use Azure-specific Pulumi stack as Licdata infrastructure stack.

    Collaborators:
        - org.acmsl.licdata.infrastructure.PulumiStack
    """

    def __init__(self, name: str, projectName: str, location: str):
        """
        Creates a new PulumiAzureStack instance.
        :param name: The name of the stack.
        :type name: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        """
        super().__init__(name, projectName, location)
        self._resource_group = None
        self._function_storage_account = None
        self._app_service_plan = None
        self._function_app = None
        self._public_ip_address = None
        self._dns_zone = None
        self._dns_record = None
        self._blob_container = None
        self._functions_package = None
        self._container_registry = None
        self._webapp_deployment_slot = None
        self._app_insights = None
        self._docker_pull_role_definition = None
        self._docker_pull_role_assignment = None

    @classmethod
    def instantiate(cls):
        """
        Creates an instance.
        :return: The new instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.PulumiAzureStackFactory
        """
        raise InvalidOperationError("Cannot instantiate PulumiAzureStack directly")

    @property
    def resource_group(self) -> ResourceGroup:
        """
        Retrieves the Azure Resource Group.
        :return: Such Resource Group.
        :rtype: ResourceGroup
        """
        return self._resource_group

    @property
    def function_storage_account(self) -> FunctionStorageAccount:
        """
        Retrieves the Azure Function Storage Account.
        :return: Such Function Storage Account.
        :rtype: FunctionStorageAccount
        """
        return self._function_storage_account

    @property
    def app_service_plan(self) -> AppServicePlan:
        """
        Retrieves the Azure App Service Plan.
        :return: Such App Service Plan.
        :rtype: AppServicePlan
        """
        return self._app_service_plan

    @property
    def function_app(self) -> FunctionApp:
        """
        Retrieves the Azure Function App.
        :return: Such Function App.
        :rtype: FunctionApp
        """
        return self._function_app

    @property
    def public_ip_address(self) -> PublicIpAddress:
        """
        Retrieves the Azure Public IP Address.
        :return: Such Public IP Address.
        :rtype: PublicIpAddress
        """
        return self._public_ip_address

    @property
    def dns_zone(self) -> DnsZone:
        """
        Retrieves the Azure DNS Zone.
        :return: Such DNS Zone.
        :rtype: DnsZone
        """
        return self._dns_zone

    @property
    def dns_record(self) -> DnsRecord:
        """
        Retrieves the Azure DNS Record.
        :return: Such DNS Record.
        :rtype: DnsRecord
        """
        return self._dns_record

    @property
    def blob_container(self) -> BlobContainer:
        """
        Retrieves the Azure Blob Container.
        :return: Such Blob Container.
        :rtype: BlobContainer
        """
        return self._blob_container

    @property
    def functions_package(self) -> FunctionsPackage:
        """
        Retrieves the Azure Functions Package.
        :return: Such Functions Package.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.FunctionsPackage
        """
        return self._functions_package

    @property
    def webapp_deployment_slot(self) -> FunctionsDeploymentSlot:
        """
        Retrieves the Azure Functions Deployment Slot.
        :return: Such Functions Deployment Slot.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.FunctionsDeploymentSlot
        """
        return self._webapp_deployment_slot

    @property
    def app_insights(self) -> AppInsights:
        """
        Retrieves the Azure App Insights instance.
        :return: Such instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.AppInsights
        """
        return self._app_insights

    @property
    def container_registry(self) -> ContainerRegistry:
        """
        Retrieves the Azure Container Registry instance.
        :return: Such instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.ContainerRegistry
        """
        return self._container_registry

    @property
    def docker_pull_role_definition(self) -> DockerPullRoleDefinition:
        """
        Retrieves the Role Definition allowing the functinos to perform Docker pulls.
        :return: Such instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.DorkecPullRoleDefinition
        """
        return self._docker_pull_role_definition

    @property
    def docker_pull_role_assignment(self) -> DockerPullRoleAssignment:
        """
        Retrieves the Role Assignment allowing the functions to perform Docker pulls.
        :return: Such instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.DockerPullRoleAssignment
        """
        return self._docker_pull_role_assignment

    def declare_infrastructure(self):
        """
        Creates the infrastructure.
        """
        self._resource_group = ResourceGroup(
            self.stack_name, self.project_name, self.location
        )
        self._function_storage_account = FunctionStorageAccount(
            self.stack_name, self.project_name, self.location, self._resource_group
        )
        self._app_service_plan = AppServicePlan(
            self.stack_name, self.project_name, self.location, self._resource_group
        )
        # self._public_ip_address = PublicIpAddress(self.stack_name, self.project_name, self.location, self._resource_group)
        # self._dns_zone = DnsZone(self.stack_name, self.project_name, self.location, self._resource_group)
        # self._dns_record = DnsRecord(
        #    self._public_ip_address,
        #    self._dns_zone,
        #    self.stack_name,
        #    self.project_name,
        #    self.location,
        #    self._resource_group,
        # )
        # self._blob_container = BlobContainer(
        #     self._function_storage_account, self.stack_name, self.project_name, self.location, self._resource_group
        # )
        # self._functions_package = FunctionsPackage(
        #     self._blob_container, self._function_storage_account, self.stack_name, self.project_name, self.location, self._resource_group
        # )
        self._app_insights = AppInsights(
            self.stack_name, self.project_name, self.location, self._resource_group
        )

        self._container_registry = ContainerRegistry(
            self.stack_name, self.project_name, self.location, self._resource_group
        )

        self._function_app = FunctionApp(
            self._app_insights,
            self._function_storage_account,
            self._app_service_plan,
            self._container_registry,
            self.stack_name,
            self.project_name,
            self.location,
            self._resource_group,
        )
        # self._webapp_deployment_slot = FunctionsDeploymentSlot(
        #     self._function_app, self._resource_group
        # )
        self._docker_pull_role_definition = DockerPullRoleDefinition(
            self._container_registry,
            self.stack_name,
            self.project_name,
            self.location,
            self._resource_group,
        )

        self._docker_pull_role_assignment = DockerPullRoleAssignment(
            self._function_app,
            self._docker_pull_role_definition,
            self._container_registry,
            self.stack_name,
            self.project_name,
            self.location,
            self._resource_group,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
