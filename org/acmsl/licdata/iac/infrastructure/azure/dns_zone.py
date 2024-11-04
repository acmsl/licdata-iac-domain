# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/dns_zone.py

This script defines the DnsZone class.

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


class DnsZone:
    """
    Azure DnsZone for Licdata.

    Class name: DnsZone

    Responsibilities:
        - Define the Azure DnsZone for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new DnsZone instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._dns_zone = self.create_dns_zone(
            "licenses", "licenses.acmsl.org", resourceGroup
        )
        self._dns_zone.name.apply(lambda name: pulumi.export("dns_zone", name))

    @property
    def dns_zone(self) -> pulumi_azure_native.network.Zone:
        """
        Retrieves the DNS zone.
        :return: Such DNS zone.
        :rtype: pulumi_azure_native.network.Zone
        """
        return self._dns_zone

    def create_dns_zone(
        self,
        name: str,
        domainName: str,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.network.Zone:
        """
        Creates a network zone.
        :param name: The name of the DNS zone.
        :type name: str
        :param domainName: The domain name.
        :type domainName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The DNS zone.
        :rtype: pulumi_azure_native.network.Zone
        """
        return pulumi_azure_native.network.Zone(
            name,
            resource_group_name=resourceGroup.name,
            zone_type="Public",
            zone_name=domainName,
            location="global",
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._dns_zone, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
