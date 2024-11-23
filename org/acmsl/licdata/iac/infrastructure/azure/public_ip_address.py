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
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class PublicIpAddress(AzureResource):
    """
    Azure PublicIpAddress for Licdata.

    Class name: PublicIpAddress

    Responsibilities:
        - Define the Azure PublicIpAddress for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        publicIpAllocationMethod: str,
        ipAddressType: str,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new PublicIpAddress instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param publicIpAllocationMethod: The public IP allocation method.
        :type publicIpAllocationMethod: str
        :param ipAddressType: The IP address type.
        :type ipAddressType: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._public_ip_allocation_method = publicIpAllocationMethod
        self._ip_address_type = ipAddressType

    @property
    def public_ip_allocation_method(self) -> str:
        """
        Gets the public IP allocation method.
        :return: The public IP allocation method.
        :rtype: str
        """
        return (
            self._public_ip_allocation_method
            if self._public_ip_allocation_method is not None
            else "Static"
        )

    @property
    def ip_address_type(self) -> str:
        """
        Gets the IP address type.
        :return: The IP address type.
        :rtype: str
        """
        return (
            self._ip_address_type if self._ip_address_type is not None else "Standard"
        )

    # @override
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
        return "pipa"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.network.PublicIPAddress:
        """
        Creates a public IP address.
        :param name: The name of the public IP address.
        :type name: str
        :return: The public IP address.
        :rtype: pulumi_azure_native.network.PublicIPAddress
        """
        return pulumi_azure_native.network.PublicIPAddress(
            name,
            resource_group_name=self.resource_group.name,
            public_ip_allocation_method=self.public_ip_allocation_method,
            sku=pulumi_azure_native.network.PublicIPAddressSkuArgs(
                name=self.ip_address_type
            ),
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.network.PublicIPAddress):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.network.PublicIPAddress
        """
        resource.ip_address.apply(lambda ip: pulumi.export("public_ip_address", ip))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
