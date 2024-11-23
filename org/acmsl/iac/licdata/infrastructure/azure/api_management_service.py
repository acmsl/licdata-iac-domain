# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/api_management_service.py

This script defines the ApiManagementService class.

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
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native
from typing import Any


class ApiManagementService(AzureResource):
    """
    Azure ApiManagementService for Licdata.

    Class name: ApiManagementService

    Responsibilities:
        - Define the Azure Api Management Service for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        publisher_email: str,
        publisher_name: str,
        sku: str,
        capacity: int,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new ApiManagementService instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param publisher_email: The email of the publisher.
        :type publisher_email: str
        :param publisher_name: The name of the publisher.
        :type publisher_name: str
        :param sku: The sku of the service.
        :type sku: str
        :param capacity: The capacity of the service.
        :type capacity: int
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._publisher_email = publisherEmail
        self._publisher_name = publisherName
        self._sku = sku
        self.capacity = capacity

    @property
    def publisher_email(self) -> str:
        """
        Retrieves the publisher's email.
        :return: The publisher's email.
        :rtype: str
        """
        return self._publisher_email

    @property
    def publisher_name(self) -> str:
        """
        Retrieves the name of the publisher.
        :return: The name.
        :rtype: str
        """
        return self._publisher_name

    @property
    def sku(self) -> str:
        """
        Retrieves the sku.
        :return: The sku.
        :rtype: str
        """
        return self._sku if self._sku is not None else "Consumption"

    @property
    def capacity(self) -> int:
        """
        Retrieves the capacity.
        :return: The capacity.
        :rtype: int
        """
        return self._capacity if self._capacity is not None else 0

    # @override
    def _resource_name(self, stackName: str, projectName: str, location: str) -> str:
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
        return "apims"

    # @override
    def _create(self, name: str) -> Any:
        """
        Creates the resource.
        :param name: The name of the resource.
        :type name: str
        :return: The resource.
        :rtype: Any
        """
        return pulumi_azure_native.apimanagement.ApiManagementService(
            name=name,
            resource_group_id=self.resource_group.id,
            publisher_email=self.publisher_email,
            publisher_name=self.publisher_name,
            sku={
                "name": self.sku,
                "capacity": self.capacity,
            },
        )

    # @override
    def _post_create(
        self, resource: pulumi_azure_native.apimanagement.ApiManagementService
    ):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.apimanagement.ApiManagementService
        """
        resource.name.apply(lambda name: pulumi.export(f"api_management_service", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
