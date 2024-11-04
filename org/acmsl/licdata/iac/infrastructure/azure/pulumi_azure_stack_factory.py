# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/pulumi_azure_stack_factory.py

This script defines the PulumiAzureStackFactory class.

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
from org.acmsl.licdata.iac.domain import StackFactory
from org.acmsl.licdata.iac.infrastructure.azure import PulumiAzureStack


class PulumiAzureStackFactory(StackFactory):
    """
    Creates Azure-specific Pulumi stacks.

    Class name: PulumiAzureStackFactory

    Responsibilities:
        - Create PulumiAzureStack instances.

    Collaborators:
        - org.acmsl.licdata.infrastructure.azure.PulumiAzureStack
    """

    def __init__(self):
        """
        Creates a new PulumiAzureStackFactory instance.
        """
        super().__init__()

    @classmethod
    def instantiate(cls):
        """
        Creates an instance.
        :return: The new instance.
        :rtype: org.acmsl.licdata.iac.infrastructure.azure.PulumiAzureStackFactory
        """
        return cls()

    def new(self, stackName: str, projectName: str, location: str) -> PulumiAzureStack:
        """
        Creates a new stack.
        :param stackName: The stack name.
        :type stackName: str
        :param projectName: The project name.
        :type projectName: str
        :param location: The location.
        :type location: str
        """
        return PulumiAzureStack(stackName, projectName, location)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
