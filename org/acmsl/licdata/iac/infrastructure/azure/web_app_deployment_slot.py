# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/web_app_deployment_slot.py

This script defines the WebAppDeploymentSlot class.

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
from pythoneda.shared import BaseObject
import pulumi
import pulumi_azure_native


class WebAppDeploymentSlot(BaseObject):
    """
    Logic to define deployment slots in Azure Webapps.

    Class name: WebAppDeploymentSlot

    Responsibilities:
        - Deployment slots for Licdata functions.

    Collaborators:
        - None
    """

    def __init__(
        self,
        name: str,
        filePath: str,
        webApp: pulumi_azure_native.web.WebApp,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new WebAppDeploymentSlot instance.
        :param name: The slot name.
        :type name: str
        :param filePath: The file path.
        :type filePath: str
        :param webApp: The web app.
        :type webApp: pulumi_azure_native.web.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._webapp_deployment_slot = self.create_webapp_deployment_slot(
            name, filePath, webApp, resourceGroup
        )
        self._webapp_deployment_slot.name.apply(
            lambda name: pulumi.export("webapp_deployment_slot", name)
        )

    @property
    def webapp_deployment_slot(self) -> pulumi_azure_native.web.WebAppDeploymentSlot:
        """
        Retrieves the webapp deployment slot.
        :return: Such slot.
        :rtype: pulumi_azure_native.web.WebAppDeploymentSlot
        """
        return self._webapp_deployment_slot

    def create_webapp_deployment_slot(
        self,
        name: str,
        filePath: str,
        webApp: pulumi_azure_native.web.WebApp,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.web.WebAppDeploymentSlot:
        """
        Creates a new WebAppDeploymentSlot instance.
        :param name: The slot name.
        :type name: str
        :param filePath: The file path.
        :type filePath: str
        :param webApp: The WebApp.
        :type webApp: pulumi_azure_native.web.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The WebAppDeploymentSlot.
        :rtype: pulumi_azure_native.web.WebAppDeploymentSlot
        """
        return pulumi_azure_native.web.WebAppDeploymentSlot(
            name,
            name=webApp.name,
            resource_group_name=resourceGroup.name,
            package=pulumi.FileAsset(filePath),
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._webapp_deployment_slot, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
