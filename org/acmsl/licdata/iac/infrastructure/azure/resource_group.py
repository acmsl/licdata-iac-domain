# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/resource_group.py

This script defines the Azure ResourceGroup resources for Licdata.

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
# Import Pulumi Azure SDK
import pulumi
import pulumi_azure_native


class ResourceGroup:
    """
    Azure ResourceGroup resources for Licdata.

    Class name: ResourceGroup

    Responsibilities:
        - Define the Azure ResourceGroup resources.

    Collaborators:
        - None
    """

    def __init__(self, location: str):
        """
        Creates a new ResourceGroup instance.
        :param location: The location of the resource group.
        :type location: str
        """
        super().__init__()
        self._resource_group = self.create_resource_group("licenses", location)
        self._resource_group.name.apply(
            lambda name: pulumi.export("resource_group", name)
        )

    @property
    def resource_group(self) -> pulumi_azure_native.resources.ResourceGroup:
        """
        Retrieves the Azure Resource Group.
        :return: Such Resource Group.
        :rtype: pulumi_azure_native.resources.ResourceGroup
        """
        return self._resource_group

    def create_resource_group(
        self, resourceGroupName: str, location: str
    ) -> pulumi_azure_native.resources.ResourceGroup:
        """
        Creates an Azure Resource Group.
        :param resourceGroupName: The name of the resource group.
        :type resourceGroupName: str
        :param location: The location of the resource group.
        :type location: str
        :return: The Azure Resource Group.
        :rtype: pulumi_azure_native.resources.ResourceGroup
        """
        return pulumi_azure_native.resources.ResourceGroup(
            resourceGroupName, location=location
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._resource_group, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
