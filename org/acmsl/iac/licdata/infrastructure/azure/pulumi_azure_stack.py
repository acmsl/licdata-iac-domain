# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/pulumi_azure_stack.py

This script defines the PulumiAzureStack class.

Copyright (C) 2024-today acmsl's Licdata IaC

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
from org.acmsl.iac.licdata.infrastructure import PulumiStack
from .functions_package import FunctionsPackage
from .functions_deployment_slot import FunctionsDeploymentSlot
from pythoneda.iac.pulumi.azure import AppInsights, AppServicePlan, BlobContainer, ContainerRegistry, DnsRecord, DnsZone, DockerPullRoleAssignment, DockerPullRoleDefinition, FunctionStorageAccount, PublicIpAddress, ResourceGroup, WebApp


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
        :rtype: pythoneda.iac.pulumi.azure.PulumiAzureStackFactory
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
        :rtype: pythoneda.iac.pulumi.azure.FunctionStorageAccount
        """
        return self._function_storage_account

    @property
    def app_service_plan(self) -> AppServicePlan:
        """
        Retrieves the Azure App Service Plan.
        :return: Such App Service Plan.
        :rtype: pythoneda.iac.pulumi.azure.AppServicePlan
        """
        return self._app_service_plan

    @property
    def web_app(self) -> WebApp:
        """
        Retrieves the Azure WebApp.
        :return: Such WebApp.
        :rtype: pythoneda.iac.pulumi.azure.WebApp
        """
        return self._web_app

    @property
    def public_ip_address(self) -> PublicIpAddress:
        """
        Retrieves the Azure Public IP Address.
        :return: Such Public IP Address.
        :rtype: pythoneda.iac.pulumi.azure.PublicIpAddress
        """
        return self._public_ip_address

    @property
    def dns_zone(self) -> DnsZone:
        """
        Retrieves the Azure DNS Zone.
        :return: Such DNS Zone.
        :rtype: pythoneda.iac.pulumi.azure.DnsZone
        """
        return self._dns_zone

    @property
    def dns_record(self) -> DnsRecord:
        """
        Retrieves the Azure DNS Record.
        :return: Such DNS Record.
        :rtype: pythoneda.iac.pulumi.azure.DnsRecord
        """
        return self._dns_record

    @property
    def blob_container(self) -> BlobContainer:
        """
        Retrieves the Azure Blob Container.
        :return: Such Blob Container.
        :rtype: pythoneda.iac.pulumi.azure.BlobContainer
        """
        return self._blob_container

    @property
    def functions_package(self) -> FunctionsPackage:
        """
        Retrieves the Azure Functions Package.
        :return: Such Functions Package.
        :rtype: pythoneda.iac.pulumi.azure.FunctionsPackage
        """
        return self._functions_package

    @property
    def webapp_deployment_slot(self) -> FunctionsDeploymentSlot:
        """
        Retrieves the Azure Functions Deployment Slot.
        :return: Such Functions Deployment Slot.
        :rtype: pythoneda.iac.pulumi.azure.FunctionsDeploymentSlot
        """
        return self._webapp_deployment_slot

    @property
    def app_insights(self) -> AppInsights:
        """
        Retrieves the Azure App Insights instance.
        :return: Such instance.
        :rtype: pythoneda.iac.pulumi.azure.AppInsights
        """
        return self._app_insights

    @property
    def container_registry(self) -> ContainerRegistry:
        """
        Retrieves the Azure Container Registry instance.
        :return: Such instance.
        :rtype: pythoneda.iac.pulumi.azure.ContainerRegistry
        """
        return self._container_registry

    @property
    def docker_pull_role_definition(self) -> DockerPullRoleDefinition:
        """
        Retrieves the Role Definition allowing the functions to perform Docker pulls.
        :return: Such instance.
        :rtype: pythoneda.iac.pulumi.azure.DorkecPullRoleDefinition
        """
        return self._docker_pull_role_definition

    @property
    def docker_pull_role_assignment(self) -> DockerPullRoleAssignment:
        """
        Retrieves the Role Assignment allowing the functions to perform Docker pulls.
        :return: Such instance.
        :rtype: pythoneda.iac.pulumi.azure.DockerPullRoleAssignment
        """
        return self._docker_pull_role_assignment

    async def declare_infrastructure(self):
        """
        Creates the infrastructure.
        """
        self._resource_group = ResourceGroup(
            self.stack_name, self.project_name, self.location
        )
        self._resource_group.create()

        self._function_storage_account = FunctionStorageAccount(
            self.stack_name, self.project_name, self.location, self._resource_group
        )
        self._function_storage_account.create()

        self._app_service_plan = AppServicePlan(
            self.stack_name,
            self.project_name,
            self.location,
            None,
            None,
            None,
            None,
            None,
            self._resource_group,
        )
        self._app_service_plan.create()

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
            self.stack_name,
            self.project_name,
            self.location,
            None,
            None,
            self._resource_group,
        )
        self._app_insights.create()

        self._container_registry = ContainerRegistry(
            self.stack_name,
            self.project_name,
            self.location,
            None,
            None,
            self._resource_group,
        )
        self._container_registry.create()

        self._web_app = WebApp(
            self.stack_name,
            self.project_name,
            self.location,
            self._app_insights,
            self._function_storage_account,
            self._app_service_plan,
            self._container_registry,
            self._resource_group,
        )
        self._web_app.create()

        # self._webapp_deployment_slot = FunctionsDeploymentSlot(
        #     self._function_app, self._resource_group
        # )
        self._docker_pull_role_definition = DockerPullRoleDefinition(
            self.stack_name,
            self.project_name,
            self.location,
            self._container_registry,
            self._resource_group,
        )
        self._docker_pull_role_definition.create()

        self._docker_pull_role_assignment = DockerPullRoleAssignment(
            self.stack_name,
            self.project_name,
            self.location,
            self._web_app,
            self._docker_pull_role_definition,
            self._container_registry,
            self._resource_group,
        )
        self._docker_pull_role_assignment.create()

        await self.build_docker_image()

        await self.push_docker_image(self._container_registry)


    async def build_docker_image(self, resourceGroup: ResourceGroup, containerRegistry: ContainerRegistry):
        """
        Builds the Docker image.
        """
        # Retrieve the registry credentials
        credentials = Output.all(resourceGroup.name, containerRegistry.name).apply(
            lambda args: containerRegistry.list_registry_credentials(
                resource_group_name=args[0],
                registry_name=args[1]
            )
        )

        # Extract the username and password
        admin_username = credentials.apply(lambda c: c.username)
        admin_password = credentials.apply(lambda c: c.passwords[0].value)

        # Define the image name using the registry's login server
        image_name = registry.login_server.apply(
            lambda login_server: f"{login_server}/my-image:latest"
        )

        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Define the path for the Dockerfile
        dockerfile_path = os.path.join(temp_dir.name, 'Dockerfile')

        # Write the Dockerfile content
        dockerfile_content = """
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true \
    GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git


# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev git libc-ares2 \
    && apt-get clean

# Set the working directory
WORKDIR /home/site/wwwroot

ADD .deps/ .

COPY requirements.txt .

RUN pip install --upgrade pip && pip install grpcio && pip install --no-cache-dir -r requirements.txt --user

ENV FUNCTIONS_WORKER_RUNTIME python

ENV PYTHONPATH="${PYTHONPATH}:/root/.local/lib/python3.11/site-packages"

EXPOSE 80
        """

        # Write the Dockerfile to the temporary directory
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content)

        # Define the path for the requirements.txt
        requirements_txt_path = os.path.join(temp_dir.name, 'requirements.txt')

        # Write the Dockerfile content
        requirements_txt_content = """
azure-functions==1.21.3
bcrypt==4.1.2
brotlicffi==1.1.0.0
certifi==2024.2.2
cffi==1.16.0
charset-normalizer==3.3.2
coverage==7.4.4
cryptography==42.0.5
dbus_next==0.2.3
ddt==1.7.2
Deprecated==1.2.14
dnspython==2.6.1
dulwich==0.21.7
esdbclient==1.1.3
gitdb==4.0.11
GitPython==3.1.43
grpcio==1.62.2
idna==3.7
installer==0.7.0
packaging==24.0
paramiko==3.4.0
path==16.14.0
poetry-core==1.9.0
protobuf==4.24.4
pyasn1==0.6.0
pycparser==2.22
PyGithub==2.3.0
PyJWT==2.8.0
PyNaCl==1.5.0
requests==2.31.0
semver==3.0.2
six==1.16.0
typing_extensions==4.11.0
unidiff==0.7.5
urllib3==2.2.1
wheel==0.43.0
wrapt==1.16.0
        """

        image_name = containerRegistry.login_server.apply(
            lambda login_server: f"{login_server}/licdata:latest"

        # Build and push the Docker image
        image = Image(
            'licdata:latest',
            build=temporary_folder,
            image_name=image_name,
            registry=Registry(
                server=containerRegistry.login_server,
                username=admin_username,
                password=admin_password
            )
        )

    async def push_docker_image(self, container_registry: ContainerRegistry):
        """
        Pushes the Docker image to the container registry.
        :param container_registry: The container registry.
        :type container_registry: ContainerRegistry
        """
        pass

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
