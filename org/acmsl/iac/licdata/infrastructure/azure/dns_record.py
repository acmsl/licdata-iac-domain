# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/dns_record.py

This script defines the DnsRecord class.

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
from .azure_resource import AzureResource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class DnsRecord(AzureResource):
    """
    Azure DnsRecord for Licdata.

    Class name: DnsRecord

    Responsibilities:
        - Define the Azure DnsRecord for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        recordType: str,
        ttl: int,
        publicIpAddress: pulumi_azure_native.network.PublicIPAddress,
        dnsZone: pulumi_azure_native.network.Zone,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Azure instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param recordType: The record type.
        :type recordType: str
        :param ttl: The TTL.
        :type ttl: int
        :param publicIpAddress: The public IP address.
        :type publicIpAddress: pulumi_azure_native.network.PublicIPAddress
        :param dnsZone: The Zone.
        :type dnsZone: pulumi_azure_native.network.Zone
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "public_ip_address": publicIpAddress,
                "dns_zone": dnsZone,
                "resource_group": resourceGroup,
            },
        )
        self._record_type = recordType
        self._ttl = ttl

    @property
    def record_type(self) -> str:
        """
        Retrieves the record type.
        :return: The record type.
        :rtype: str
        """
        return self._record_type if self._record_type is not None else "A"

    @property
    def ttl(self) -> int:
        """
        Retrieves the TTL.
        :return: The TTL.
        :rtype: int
        """
        return self._ttl if self._ttl is not None else 3600

        self._dns_record = self.create_dns_record(
            "api", dnsZone, resourceGroup, "A", 3600, publicIpAddress.ip_address
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
        return "dnsr"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.network.RecordSet:
        """
        Creates an A record.
        :param name: The name of the A record.
        :param name: The name of the resource.
        :type name: str
        :return: The DNS record.
        :rtype: pulumi_azure_native.network.RecordSet
        """
        return pulumi_azure_native.network.RecordSet(
            resource_name=name,
            zone_name=self.dns_zone.name,
            resource_group_name=self.resource_group.name,
            record_type=self.record_type,
            relative_record_set_name=name,
            ttl=self.ttl,
            a_records=[
                pulumi_azure_native.network.ARecordArgs(
                    ipv4_address=self.public_ip_address.ip_address
                )
            ],
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.network.RecordSet):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.network.RecordSet
        """
        resource.name.apply(lambda name: pulumi.export("dns_record", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
