# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/dns_record.py

This script defines the DnsRecord class.

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
from typing import List


class DnsRecord(BaseObject):
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
        publicIpAddress: pulumi_azure_native.network.PublicIPAddress,
        dnsZone: pulumi_azure_native.network.Zone,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Azure instance.
        :param publicIpAddress: The public IP address.
        :type publicIpAddress: pulumi_azure_native.network.PublicIPAddress
        :param dnsZone: The Zone.
        :type dnsZone: pulumi_azure_native.network.Zone
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()

        self._dns_record = self.create_dns_record(
            "api", dnsZone, resourceGroup, "A", 3600, publicIpAddress.ip_address
        )
        self._dns_record.name.apply(lambda name: pulumi.export("dns_record", name))

    @property
    def dns_record(self) -> pulumi_azure_native.network.RecordSet:
        """
        Retrieves the DNS record.
        :return: Such DNS record.
        :rtype: pulumi_azure_native.network.RecordSet
        """
        return self._dns_record

    def create_dns_record(
        self,
        name: str,
        zone: pulumi_azure_native.network.Zone,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        recordType: str,
        ttl: int,
        ipAddress: str,
    ) -> pulumi_azure_native.network.RecordSet:
        """
        Creates an A record.
        :param name: The name of the A record.
        :type name: str
        :param zone: The network zone.
        :type zone: pulumi_azure_native.network.Zone
        :param resourceGroup: The resource group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param recordType: The record type.
        :type recordType: str
        :param ttl: The TTL.
        :type ttl: int
        :param ipAddress: The IP address.
        :type ipAddress: str
        :return: The A record.
        :rtype: pulumi_azure_native.network.RecordSet
        """
        return pulumi_azure_native.network.RecordSet(
            resource_name=name,
            zone_name=zone.name,
            resource_group_name=resourceGroup.name,
            record_type=recordType,
            relative_record_set_name=name,
            ttl=ttl,
            a_records=[pulumi_azure_native.network.ARecordArgs(ipv4_address=ipAddress)],
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._dns_record, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
