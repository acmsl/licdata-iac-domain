# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/domain/stack.py

This script defines the Stack class.

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
import abc
from pythoneda.shared import BaseObject, Port, primary_key_attribute


class Stack(Port, BaseObject):
    """
    A Licdata infrastructure stack.

    Class name: Stack

    Responsibilities:
        - Represent a Licdata infrastructure stack.

    Collaborators:
        - org.acmsl.licdata.domain.LicdataIac
    """

    def __init__(self, stackName: str, projectName: str, location: str):
        """
        Creates a new stack instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        """
        super().__init__()
        self._stack_name = stackName
        self._project_name = projectName
        self._location = location

    @property
    @primary_key_attribute
    def stack_name(self) -> str:
        """
        Retrieves the stack name.
        :return: The name of the stack.
        :rtype: str
        """
        return self._stack_name

    @property
    @primary_key_attribute
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
        Retrieves the location.
        :return: The location.
        :rtype: str
        """
        return self._location

    @abc.abstractmethod
    async def up(self):
        """
        Brings up the stack.
        """
        pass


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
