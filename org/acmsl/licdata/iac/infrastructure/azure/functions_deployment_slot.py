# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/functions_deployment_slot.py

This script defines the FunctionsDeploymentSlot class.

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
from .web_app_deployment_slot import WebAppDeploymentSlot
import pulumi
import pulumi_azure_native


class FunctionsDeploymentSlot(WebAppDeploymentSlot):
    """
    Logic to define Licdata's functions deployment slots in Azure Webapps.

    Class name: FunctionsDeploymentSlot

    Responsibilities:
        - Deployment slots for Licdata functions.

    Collaborators:
        - None
    """

    def __init__(
        self,
        webApp: pulumi_azure_native.web.WebApp,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new WebAppDeploymentSlot instance.
        :param webApp: The web app.
        :type webApp: pulumi_azure_native.web.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__("license_functions", "./rest.zip", webApp, resourceGroup)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
