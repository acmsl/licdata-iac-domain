# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/api.py

This script defines the Api class.

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


class Api:
    """
    Azure Api for Licdata.

    Class name: Api

    Responsibilities:
        - Define the Azure Api for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        apiManagementService: pulumi_azure_native.apimanagement.ApiManagementService,
    ):
        """
        Creates a new Api instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param apiManagementService: The ApiManagementService.
        :type apiManagementService: pulumi_azure_native.apimanagement.ApiManagementService
        """
        super().__init__()
        self._api = self.create_api(
            "licensesApi",
            resourceGroup,
            apiManagementService,
            "licenses",
            "Licenses API",
        )
        self._api.name.apply(lambda name: pulumi.export("api", name))

    @property
    def api(self) -> pulumi_azure_native.apimanagement.Api:
        """
        Retrieves the API.
        :return: Such API.
        :rtype: pulumi_azure_native.apimanagement.Api
        """
        return self._api

    def create_api(
        self,
        name: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        apiManagementService: pulumi_azure_native.apimanagement.ApiManagementService,
        path: str,
        displayName: str,
    ) -> pulumi_azure_native.apimanagement.Api:
        """
        Creates an API.
        :param name: The name of the API.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param apiManagementService: The API Management Service.
        :type apiManagementService: pulumi_azure_native.apimanagement.ApiManagementService
        :param path: The path of the API.
        :type path: str
        :param displayName: The display name of the API.
        :type displayName: str
        :return: The API.
        :rtype: pulumi_azure_native.apimanagement.Api
        """
        return pulumi_azure_native.apimanagement.Api(
            name,
            resource_group_name=resourceGroup.name,
            service_name=apiManagementService.name,
            path=path,
            protocols=["https"],
            display_name=displayName,
        )

        def __getattr__(self, attr):
            """
            Delegates attribute/method lookup to the wrapped instance.
            :param attr: The attribute.
            :type attr: Any
            """
            return getattr(self._api, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
