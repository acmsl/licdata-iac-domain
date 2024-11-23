# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/api.py

This script defines the Api class.

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
from pythoneda.iac.pulumi.azure import Api, ApiManagementService, ResourceGroup


class LicdataApi(Api):
    """
    Azure Api for Licdata.

    Class name: Api

    Responsibilities:
        - Define the Azure Api for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        apiManagementService: ApiManagementService,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Api instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param apiManagementService: The ApiManagementService.
        :type apiManagementService: org.acmsl.iac.licdata.infrastructure.azure.ApiManagementService
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            "licenses",
            ["https"],
            apiManagementService,
            resourceGroup,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
