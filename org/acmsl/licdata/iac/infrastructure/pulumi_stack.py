# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/pulumi_stack.py

This script defines the PulumiStack class.

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
from org.acmsl.licdata.iac.domain import Stack
from pulumi import automation as auto
from pulumi.automation.errors import CommandError
from org.acmsl.licdata.iac.domain import InfrastructureUpdated


class PulumiStack(Stack, abc.ABC):
    """
    Pulumi implementation of Licdata infrastructure stacks.

    Class name: PulumiStack

    Responsibilities:
        - Use Pulumi stack as Licdata infrastructure stack.

    Collaborators:
        - org.acmsl.licdata.domain.Stack
    """

    def __init__(self, stackName: str, projectName: str, location: str):
        """
        Creates a new PulumiStack instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        """
        super().__init__(stackName, projectName, location)

    async def up(self):
        """
        Brings up the stack.
        """

        def declare_infrastructure_wrapper():
            return self.declare_infrastructure()

        result = None

        stack = auto.create_or_select_stack(
            stack_name=self.stack_name,
            project_name=self.project_name,
            program=declare_infrastructure_wrapper,
        )

        # stack.workspace.install_plugin("azure-native", "v2.11.0")
        stack.set_config("azure-native:location", auto.ConfigValue(value=self.location))
        stack.refresh(on_output=self.__class__.logger().debug)

        try:
            outcome = stack.up(on_output=self.__class__.logger().debug)
            import json

            self.__class__.logger().info(
                f"update summary: \n{json.dumps(outcome.summary.resource_changes, indent=4)}"
            )
            result = InfrastructureUpdated(
                self.stack_name, self.project_name, self.location
            )
        except CommandError as e:
            self.__class__.logger().error(f"CommandError: {e}")

        return result

    @abc.abstractmethod
    def declare_infrastructure(self):
        """
        Declares the infrastructure.
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
