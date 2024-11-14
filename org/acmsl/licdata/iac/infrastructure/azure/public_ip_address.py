# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/public_ip_address.py

This script defines the PublicIpAddress class.

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


class PublicIpAddress(BaseObject):
    """
    Azure PublicIpAddress for Licdata.

    Class name: PublicIpAddress

    Responsibilities:
        - Define the Azure PublicIpAddress for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new PublicIpAddress instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._public_ip_address = self.create_public_ip_address(
            "licenses", resourceGroup
        )
        self._public_ip_address.ip_address.apply(
            lambda ip: pulumi.export("public_ip_address", ip)
        )

    @property
    def public_ip_address(self) -> pulumi_azure_native.network.PublicIPAddress:
        """
        Retrieves the public IP address.
        :return: Such public IP address.
        :rtype: pulumi_azure_native.network.PublicIPAddress
        """
        return self._public_ip_address

    def create_public_ip_address(
        self, name: str, resourceGroup: pulumi_azure_native.resources.ResourceGroup
    ) -> pulumi_azure_native.network.PublicIPAddress:
        """
        Creates a public IP address.
        :param name: The name of the public IP address.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The public IP address.
        :rtype: pulumi_azure_native.network.PublicIPAddress
        """
        return pulumi_azure_native.network.PublicIPAddress(
            name,
            resource_group_name=resourceGroup.name,
            public_ip_allocation_method="Static",
            sku=pulumi_azure_native.network.PublicIPAddressSkuArgs(name="Standard"),
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._public_ip_address, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
