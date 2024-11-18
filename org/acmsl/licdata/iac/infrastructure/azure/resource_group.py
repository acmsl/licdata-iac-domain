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
from org.acmsl.licdata.iac.domain import Resource
import pulumi
import pulumi_azure_native
from typing import override


class ResourceGroup(Resource):
    """
    Azure ResourceGroup resources for Licdata.

    Class name: ResourceGroup

    Responsibilities:
        - Define the Azure ResourceGroup resources.

    Collaborators:
        - None
    """

    def __init__(self, stackName: str, projectName: str, location: str):
        """
        Creates a new ResourceGroup instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        """
        super().__init__(stackName, projectName, location, {})

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
        return f"{stackName}-{projectName}-{location}-resource-group"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.resources.ResourceGroup:
        """
        Creates an Azure Resource Group.
        :param name: The name of the resource group.
        :type name: str
        :return: The Azure Resource Group.
        :rtype: pulumi_azure_native.resources.ResourceGroup
        """
        return pulumi_azure_native.resources.ResourceGroup(
            name, location=self.location, resource_group_name=name
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.resources.ResourceGroup):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.resources.ResourceGroup
        """
        resource.name.apply(lambda name: pulumi.export("resource_group", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
