# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/container_registry.py

This script defines the ContainerRegistry class.

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


class ContainerRegistry:
    """
    Azure Container Registry for Licdata.

    Class name: ContainerRegistry

    Responsibilities:
        - Define the Azure Container Registry for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Api instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param apiManagementService: The ApiManagementService.
        :type apiManagementService: pulumi_azure_native.apimanagement.ApiManagementService
        """
        super().__init__()
        self._container_registry = self.create_container_registry(
            "licenses", resourceGroup
        )
        self._container_registry.name.apply(
            lambda name: pulumi.export("licenses_container_registry", name)
        )

    @property
    def container_registry(self) -> pulumi_azure_native.containerregistry.Registry:
        """
        Retrieves the container registry.
        :return: Such instance.
        :rtype: pulumi_azure_native.containerregistry.Registry
        """
        return self._container_registry

    def create_container_registry(
        self,
        name: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.containerregistry.Registry:
        """
        Creates a container registry.
        :param name: The name of the registry.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The container registry.
        :rtype: pulumi_azure_native.containerregistry.Registry
        """
        return pulumi_azure_native.containerregistry.Registry(
            name,
            resource_group_name=resourceGroup.name,
            registry_name=name,
            sku=pulumi_azure_native.containerregistry.SkuArgs(
                name="Basic",  # Available SKUs are Basic, Standard, Premium
            ),
            admin_user_enabled=True,  # Enable admin user for easier authentication (optional)
            location=resourceGroup.location,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._container_registry, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
