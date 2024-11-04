# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/api_management_service.py

This script defines the ApiManagementService class.

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


class ApiManagementService:
    """
    Azure ApiManagementService for Licdata.

    Class name: ApiManagementService

    Responsibilities:
        - Define the Azure Api Management Service for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new ApiManagementService instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._api_management_service = self.create_api_managenent_service(
            "licenses",
            self.resource_group,
            "admin@example.com",
            "admin",
            "Consumption",
            0,
        )
        self._api_management_service.name.apply(
            lambda name: pulumi.export(f"api_management_service", name)
        )

    @property
    def api_management_service(
        self,
    ) -> pulumi_azure_native.apimanagement.ApiManagementService:
        """
        Retrieves the API Management Service.
        :return: Such API Management Service.
        :rtype: pulumi_azure_native.apimanagement.ApiManagementService
        """
        return self._api_management_service

    def create_api_managenent_service(
        self,
        name: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        email: str,
        password: str,
        sku: str,
        capacity: int,
    ) -> pulumi_azure_native.apimanagement.ApiManagementService:
        """
        Creates an Azure Api Management Service.
        :param name: The name of the service.
        :type name: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param email: The email of the service.
        :type email: str
        :param password: The password of the service.
        :type password: str
        :param sku: The sku of the service.
        :type sku: str
        :param capacity: The capacity of the service.
        :type capacity: int
        :return: The ApiManagementService instance.
        :rtype: pulumi_azure_native.apimanagement.ApiManagementService
        """
        return pulumi_azure_native.apimanagement.ApiManagementService(
            name=name,
            resource_group_id=resourceGroup.id,
            publisher_email=email,
            publisher_name=name,
            sku={
                "name": sku,
                "capacity": capacity,
            },
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._api_management_service, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
