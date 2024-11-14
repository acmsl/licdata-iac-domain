# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/front_door.py

This script defines the FrontDoor class.

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
from typing import List


class FrontDoor(BaseObject):
    """
    Azure FrontDoor for Licdata.

    Class name: FrontDoor

    Responsibilities:
        - Define the Azure FrontDoor for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Front Door.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()

        self._front_door = self.create_front_door(
            "licenseApi", "licenseApiProfile", resourceGroup
        )
        self._front_door.name.apply(lambda name: pulumi.export("front_door", name))

    @property
    def front_door(self) -> pulumi_azure_native.cdn.Profile:
        """
        Retrieves the front door.
        :return: The front door.
        :rtype: pulumi_azure_native.cdn.Profile
        """
        return self._front_door

    def create_front_door(
        self,
        name: str,
        profileName: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.cdn.Profile:
        """
        Creates a Front Door.
        :param name: The name of the front door.
        :type name: str
        :param profileName: The name of the profile.
        :type profileName: str
        :param resourceGroup: The resource group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Front Door instance.
        :rtype: pulumi_azure_native.cdn.Profile
        """
        return pulumi_azure_native.cdn.Profile(
            name,
            resource_group_name=resourceGroup.name,
            profile_name=profileName,
            sku=pulumi_azure_native.cdn.SkuArgs(name="Standard_AzureFrontDoor"),
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._front_door, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
