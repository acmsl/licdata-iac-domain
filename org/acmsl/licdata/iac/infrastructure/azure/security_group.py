# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/security_group.py

This script defines the SecurityGroup class.

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
import pulumi
import pulumi_azure_native
from typing import List


class SecurityGroup:
    """
    Azure Security Group for Licdata.

    Class name: SecurityGroup

    Responsibilities:
        - Define the Azure Security Group for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new SecurityGroup instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._security_group = self.create_network_security_group(
            "functionSecurityGroup",
            resourceGroup,
            self.create_security_rule_args_for_accessing_cosmosdb(),
        )
        self._security_group.name.apply(
            lambda name: pulumi.export("security_group", name)
        )

    @property
    def security_group(self) -> pulumi_azure_native.network.NetworkSecurityGroup:
        """
        Retrieves the security group.
        :return: Such security group.
        :rtype: pulumi_azure_native.network.NetworkSecurityGroup
        """
        return self._security_group

    def create_security_rule_args_for_accessing_cosmosdb(
        self,
    ) -> pulumi_azure_native.network.SecurityRuleArgs:
        """
        Creates a security rule args for accessing CosmosDB.
        :return: The security rule.
        :rtype: network.SecurityRule
        """
        return pulumi_azure_native.network.SecurityRuleArgs(
            name="AllowFunctionsToCosmosDB",
            priority=100,
            direction="Inbound",
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range="443",
            source_address_prefix="*",
            destination_address_prefix="CosmosDB",
        )

    def create_network_security_group(
        self,
        name: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        securityRuleArgs: List[pulumi_azure_native.network.SecurityRuleArgs],
    ) -> pulumi_azure_native.network.NetworkSecurityGroup:
        return pulumi_azure_native.network.NetworkSecurityGroup(
            name,
            resource_group_name=resourceGroup.name,
            security_rules=securityRuleArgs,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._security_group, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
