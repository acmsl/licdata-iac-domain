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
from org.acmsl.licdata.iac.domain import Resource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native
from typing import override


class FrontDoor(Resource):
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
        stackName: str,
        projectName: str,
        location: str,
        profileName: str,
        frontDoorType: str,
        resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup,
    ):
        """
        Creates a new FrontDoor instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param profileName: The name of the profile.
        :type profileName: str
        :param frontDoorType: The type of the front door.
        :type frontDoorType: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._profile_name = profileName
        self._front_door_type = frontDoorType

    @property
    def profile_name(self) -> str:
        """
        Retrieves the name of the profile.
        :return: Such name.
        :rtype: str
        """
        return self._profile_name

    @property
    def front_door_type(self) -> str:
        """
        Retrieves the type of the front door.
        :return: Such type.
        :rtype: str
        """
        return (
            self._front_door_type
            if self._front_door_type is not None
            else "Standard_AzureFrontDoor"
        )

    # @override
    def _create(self, name: str) -> pulumi_azure_native.cdn.Profile:
        """
        Creates a Front Door.
        :param name: The name of the front door.
        :type name: str
        :return: The Front Door instance.
        :rtype: pulumi_azure_native.cdn.Profile
        """
        return pulumi_azure_native.cdn.Profile(
            name,
            resource_group_name=self.resource_group.name,
            profile_name=self.profile_name,
            sku=pulumi_azure_native.cdn.SkuArgs(name=self.front_door_type),
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.cdn.Profile):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.cdn.Profile
        """
        resource.name.apply(lambda name: pulumi.export("front_door", name))

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._front_door, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
