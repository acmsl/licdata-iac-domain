# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/role_definition.py

This script defines the RoleDefinition class.

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
import abc
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
from pythoneda.shared import BaseObject
import pulumi
import pulumi_azure_native
from typing import Dict, List


class RoleDefinition(AzureResource, abc.ABC):
    """
    Azure Role Definition for Licdata's Functions.

    Class name: RoleDefinition

    Responsibilities:
        - Common logic to define Azure Roles for Licdata's Functions.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        roleName: str,
        description: str,
        scope: str,
        assignableScopes: List[str],
        permissions: List[Dict[str, List[str]]],
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new RoleDefinition instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param roleName: The name of the role.
        :type roleName: str
        :param description: The description.
        :type description: str
        :param scope: The id of the scope.
        :type scope: str
        :param assignableScopes: The list of assignable scopes.
        :type assignableScopes: List[str]
        :param permissions: The permissions to grant.
        :type permissions: List[Dict[str, List[str]]]
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {"resource_group": resourceGroup},
        )
        self._role_name = roleName
        self._description = description
        self._scope = scope
        self._assignable_scopes = assignableScopes
        self._permissions = permissions

    @property
    def role_name(self) -> str:
        """
        Retrieves the role name.
        :return: Such name.
        :rtype: str
        """
        return self._role_name

    @property
    def description(self) -> str:
        """
        Retrieves the description.
        :return: Such information.
        :rtype: str
        """
        return self._description

    @property
    def scope(self) -> str:
        """
        Retrieves the id of the scope.
        :return: Such id.
        :rtype: str
        """
        return self._scope

    @property
    def assignable_scopes(self) -> List[str]:
        """
        Retrieves the assignable scopes.
        :return: Such ids.
        :rtype: List[str]
        """
        return self._assignable_scopes

    @property
    def permissions(self) -> List[Dict[str, List[str]]]:
        """
        Retrieves the permissions to grant.
        :return: Such permissions.
        :rtype: List[Dict[str, List[str]]]
        """
        return self._permissions

    # @override
    def _create(self, name: str) -> pulumi_azure_native.authorization.RoleDefinition:
        """
        Creates a role definition for performing docker pulls.
        :param name: The name of the role.
        :type name: str
        :return: The Azure Function App.
        :rtype: pulumi_azure_native.authorization.RoleDefinition
        """
        return pulumi_azure_native.authorization.RoleDefinition(
            name,
            role_name=self.role_name,
            description=self.description,
            assignable_scopes=self.assignable_scopes,
            permissions=self.permissions,
            scope=self.scope,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
