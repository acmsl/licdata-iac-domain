# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/domain/infrastructure_update_requested.py

This file declares the InfrastructureUpdateRequested event.

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
from pythoneda.shared import Event, primary_key_attribute
from typing import List


class InfrastructureUpdateRequested(Event):
    """
    Represents the moment an infrastructure update is requested.

    Class name: InfrastructureUpdateRequested

    Responsibilities:
        - Wraps all contextual information of the event.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        previousEventIds: List[str] = None,
        reconstructedId: str = None,
        reconstructedPreviousEventIds: List[str] = None,
    ):
        """
        Creates a new InfrastructureUpdateRequested instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The location.
        :type location: str
        :param previousEventIds: The id of previous events, if any.
        :type previousEventIds: List[str]
        :param reconstructedId: The id of the event, if it's generated externally.
        :type reconstructedId: str
        :param reconstructedPreviousEventIds: The id of the previous events, if an external event
        is being reconstructed.
        :type reconstructedPreviousEventIds: List[str]
        """
        super().__init__(
            previousEventIds, reconstructedId, reconstructedPreviousEventIds
        )
        self._stack_name = stackName
        self._project_name = projectName
        self._location = location

    @property
    @primary_key_attribute
    def stack_name(self) -> str:
        """
        Retrieves the name of the stack.
        :return: Such name.
        :rtype: str
        """
        return self._stack_name

    @property
    @primary_key_attribute
    def project_name(self) -> str:
        """
        Retrieves the name of the project.
        :return: Such name.
        :rtype: str
        """
        return self._project_name

    @property
    def location(self) -> str:
        """
        Retrieves the location.
        :return: Such location.
        :rtype: str
        """
        return self._location


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
