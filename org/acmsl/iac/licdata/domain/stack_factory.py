# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/domain/pulumi_azure_stack_factory.py

This script defines the StackFactory class.

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
from .stack import Stack
import abc
from pythoneda.shared import BaseObject, Port


class StackFactory(Port, BaseObject):
    """
    Creates stacks.

    Class name: StackFactory

    Responsibilities:
        - Create Stack instances.

    Collaborators:
        - org.acmsl.licdata.domain.Stack
    """

    def __init__(self):
        """
        Creates a new StackFactory instance.
        """
        super().__init__()

    @abc.abstractmethod
    def new(self, stackName: str, projectName: str, location: str) -> Stack:
        """
        Creates a new stack.
        :param stackName: The stack name.
        :type stackName: str
        :param projectName: The project name.
        :type projectName: str
        :param location: The location.
        :type location: str
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
