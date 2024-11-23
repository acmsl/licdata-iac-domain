# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/network_security_group.py

This script defines the NetworkSecurityGroup class.

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


class NetworkSecurityGroup(AzureResource):
    """
    Azure Security Group for Licdata.

    Class name: NetworkSecurityGroup

    Responsibilities:
        - Define the Azure Security Group for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        priority: int,
        direction: str,
        access: str,
        protocol: str,
        sourcePortRange: str,
        destinationPortRange: str,
        sourceAddressPrefix: str,
        destinationAddressPrefix: str,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new SecurityGroup instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param priority: The priority.
        :type priority: int
        :param direction: The direction.
        :type direction: str
        :param access: The access.
        :type access: str
        :param protocol: The protocol.
        :type protocol: str
        :param sourcePortRange: The source port range.
        :type sourcePortRange: str
        :param destinationPortRange: The destination port range.
        :type destinationPortRange: str
        :param sourceAddressPrefix: The source address prefix.
        :type sourceAddressPrefix: str
        :param destinationAddressPrefix: The destination address prefix.
        :type destinationAddressPrefix: str
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._priority = priority
        self._direction = direction
        self._access = access
        self._protocol = protocol
        self._source_port_range = sourcePortRange
        self._destination_port_range = destinationPortRange
        self._source_address_prefix = sourceAddressPrefix
        self._destination_address_prefix = destinationAddressPrefix

    @property
    def priority(self) -> int:
        """
        Retrieves the priority.
        :return: The priority.
        :rtype: int
        """
        return self._priority if self._priority is not None else 100

    @property
    def direction(self) -> str:
        """
        Retrieves the direction.
        :return: The direction.
        :rtype: str
        """
        return self._direction if self._direction is not None else "Inbound"

    @property
    def access(self) -> str:
        """
        Retrieves the access.
        :return: The access.
        :rtype: str
        """
        return self._access if self._access is not None else "Allow"

    @property
    def protocol(self) -> str:
        """
        Retrieves the protocol.
        :return: The protocol.
        :rtype: str
        """
        return self._protocol if self._protocol is not None else "Tcp"

    @property
    def source_port_range(self) -> str:
        """
        Retrieves the source port range.
        :return: The source port range.
        :rtype: str
        """
        return self._source_port_range if self._source_port_range is not None else "*"

    @property
    def destination_port_range(self) -> str:
        """
        Retrieves the destination port range.
        :return: The destination port range.
        :rtype: str
        """
        return (
            self._destination_port_range
            if self._destination_port_range is not None
            else "443"
        )

    @property
    def source_address_prefix(self) -> str:
        """
        Retrieves the source address prefix.
        :return: The source address prefix.
        :rtype: str
        """
        return (
            self._source_address_prefix
            if self._source_address_prefix is not None
            else "*"
        )

    @property
    def destination_address_prefix(self) -> str:
        """
        Retrieves the destination address prefix.
        :return: The destination address prefix.
        :rtype: str
        """
        return (
            self._destination_address_prefix
            if self._destination_address_prefix is not None
            else ""
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
        return "nsg"

    def create_security_rule_args(
        self, name: str
    ) -> pulumi_azure_native.network.SecurityRuleArgs:
        """
        Creates a security rule args instance.
        :param name: The name of the resource.
        :type name: str
        :return: The security rule args.
        :rtype: pulumi_azure_native.network.SecurityRuleArgs
        """
        return pulumi_azure_native.network.SecurityRuleArgs(
            name=name,
            priority=self.priority,
            direction=self.direction,
            access=self.access,
            protocol=self.protocol,
            source_port_range=self.source_port_range,
            destination_port_range=self.destination_port_range,
            source_address_prefix=self.source_address_prefix,
            destination_address_prefix=self.destination_address_prefix,
        )

    # @override
    def _create(self, name: str) -> pulumi_azure_native.network.NetworkSecurityGroup:
        """
        Creates a network security group.
        :param name: The name of the resource.
        :type name: str
        :return: The resource.
        :rtype: pulumi_azure_native.network.NetworkSecurityGroup
        """
        return pulumi_azure_native.network.NetworkSecurityGroup(
            name,
            resource_group_name=self.resource_group.name,
            security_rules=self.create_security_rule_args(name),
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.network.NetworkSecurityGroup):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.network.NetworkSecurityGroup
        """
        resource.name.apply(lambda name: pulumi.export("network_security_group", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
