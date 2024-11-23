# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/azure_resource.py

This script defines the AzureResource class.

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
from org.acmsl.iac.licdata.domain import Resource
import abc
from typing import Any, Dict


class AzureResource(Resource, abc.ABC):
    """
    Azure resources.

    Class name: AzureResource

    Responsibilities:
        - Represent an infrastructure resource in Azure.

    Collaborators:
        - None
    """

    _location_abbrevs = {"westeurope": "we", "unknown": "unk"}

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        dependencies: Dict[str, Any],
    ):
        """
        Creates a new Resource instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param dependencies: The dependencies.
        :type dependencies: Dict[str, Any]
        """
        super().__init__(stackName, projectName, location, dependencies)

    @property
    def max_length(self) -> int:
        """
        The maximum length of the resource name.
        :return: The maximum length.
        :rtype: int
        """
        return 16

    @classmethod
    def _location_abbrev(cls, location: str) -> str:
        """
        Abbreaviates the location.
        :param location: The location.
        :type location: str
        :return: The abbreviated location.
        :rtype: str
        """
        return cls._location_abbrevs.get(location, cls._location_abbrevs["unknown"])


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
