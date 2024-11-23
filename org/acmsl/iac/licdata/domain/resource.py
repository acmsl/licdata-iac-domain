# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/domain/resource.py

This script defines the Resource class.

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
from pythoneda.shared import BaseObject
import abc
from typing import Any, Dict


class Resource(BaseObject, abc.ABC):
    """
    Infrastructure resource.

    Class name: Resource

    Responsibilities:
        - Represent an infrastructure resource.
        - Know how to build the resource name based on the stack information.

    Collaborators:
        - None
    """

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
        super().__init__()
        self._stack_name = stackName
        self._project_name = projectName
        self._location = location
        self._dependencies = dependencies
        for name, value in dependencies.items():
            setattr(self, name, value)
        self._actual_resource = None

    @property
    def stack_name(self) -> str:
        """
        Retrieves the stack name.
        :return: The name of the stack.
        :rtype: str
        """
        return self._stack_name

    @property
    def project_name(self) -> str:
        """
        Retrieves the project name.
        :return: The name of the project.
        :rtype: str
        """
        return self._project_name

    @property
    def location(self) -> str:
        """
        Retrieves the Azure location.
        :return: The Azure location.
        :rtype: str
        """
        return self._location

    @property
    def dependencies(self) -> Dict[str, Any]:
        """
        Retrieves the dependencies.
        :return: The dependencies.
        :rtype: Dict[str, Any]
        """
        return self._dependencies

    @property
    def actual_resource(self) -> Any:
        """
        Retrieves the actual resource.
        :return: The actual resource.
        :rtype: Any
        """
        if self._actual_resource is None:
            self.create()

        return self._actual_resource

    def create(self) -> Any:
        """
        Creates the resource.
        :return: The actual resource.
        :rtype: Any
        """
        name = self._build_name(self.stack_name, self.project_name, self.location)
        self._actual_resource = self._create(name)
        self._post_create(self._actual_resource)

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
        return self._truncate_name(
            stackName,
            projectName,
            location,
            self._resource_name(stackName, projectName, location),
            self.max_length,
        )

    @classmethod
    @abc.abstractmethod
    def _location_abbrev(cls, location: str) -> str:
        """
        Abbreaviates the location.
        :param location: The location.
        :type location: str
        :return: The abbreviated location.
        :rtype: str
        """
        pass

    @property
    def max_length(self) -> int:
        """
        Returns the maximum length allowed for naming this resource.
        :return: The maximum length.
        :rtype: int
        """
        raise NotImplementedError("max_length property must be implemented.")

    def _truncate_name(
        self, stackName: str, projectName: str, location: str, name: str, maxLength: int
    ) -> str:
        """
        Builds the resource name prefix.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param name: The resource name.
        :type name: str
        :param maxLength: The maximum length.
        :type maxLength: int
        :return: The resource name prefix.
        :rtype: str
        """
        location_abbrev = self._location_abbrev(location)

        # Calculate fixed lengths: stack initial, dots, and location abbreviation
        fixed_length = len(projectName) + len(location_abbrev) + 1  # stack name initial

        # Determine maximum length allowed for name
        max_name_length = maxLength - fixed_length

        # Truncate name if it exceeds the maximum allowed length
        name_truncated = name[:max_name_length]
        return f"{stackName[0]}{projectName}{location_abbrev}{name_truncated}"

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    def _create(self, name: str) -> Any:
        """
        Creates the resource.
        :param name: The name of the resource.
        :type name: str
        :return: The resource.
        :rtype: Any
        """
        pass

    @abc.abstractmethod
    def _post_create(self, resource: Any):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: Any
        """
        pass

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self.actual_resource, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
