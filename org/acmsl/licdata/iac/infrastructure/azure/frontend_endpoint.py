# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/frontend_endpoint.py

This script defines the FrontendEndpoint class.

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


class FrontendEndpoint:
    """
    Azure FrontendEndpoint for Licdata.

    Class name: FrontendEndpoint

    Responsibilities:
        - Define the Azure FrontendEndpoint for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        frontDoor: pulumi_azure_native.cdn.Profile,
        dnsRecord: pulumi_azure_native.network.RecordSet,
        dnsZone: pulumi_azure_native.network.Zone,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new Frontend Endpoint.
        :param frontDoor: The Front Door.
        :type frontDoor: pulumi_azure_native.cdn.Profile
        :param dnsRecord: The DNS record for the endpoint.
        :type dnsRecord: pulumi_azure_native.network.RecordSet
        :param dnsZone: The DNS zone.
        :type dnsZone: pulumi_azure_native.network.Zone
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()

        self._frontend_endpoint = self.create_frontend_endpoint(
            "license", "licenseEndpoint", frontDoor, dnsRecord, dnsZone, resourceGroup
        )
        self._frontend_endpoint.name.apply(
            lambda name: pulumi.export("frontend_endpoint", name)
        )

    @property
    def frontend_endpoint(self) -> pulumi_azure_native.cdn.AFDEndpoint:
        """
        Retrieves the frontend endpoint.
        :return: The frontend endpoint.
        :rtype: pulumi_azure_native.cdn.AFDEndpoint
        """
        return self._frontend_endpoint

    def create_frontend_endpoint(
        self,
        name: str,
        endpointName: str,
        frontDoor: pulumi_azure_native.cdn.Profile,
        dnsRecord: pulumi_azure_native.network.RecordSet,
        dnsZone: pulumi_azure_native.network.Zone,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.cdn.AFDEndpoint:
        """
        Creates a Front Door.
        :param name: The name of the frontend endpoint.
        :type name: str
        :param endpointName: The name of the endpoint.
        :type endpointName: str
        :param frontDoor: The Front Door.
        :type frontDoor: pulumi_azure_native.cdn.Profile
        :param dnsRecord: The DNS record for the endpoint.
        :type dnsRecord: pulumi_azure_native.network.RecordSet
        :param dnsZone: The DNS zone.
        :type dnsZone: pulumi_azure_native.network.Zone
        :param resourceGroup: The resource group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The FrontendEndpoint instance.
        :rtype: pulumi_azure_native.cdn.AFDEndpoint
        """
        # Construct the FQDN using the record set name and the DNS zone name
        fqdn = pulumi.Output.concat(dnsRecord.name, ".", dnsZone.name)

        return pulumi_azure_native.cdn.AFDEndpoint(
            name,
            resource_group_name=resourceGroup.name,
            profile_name=frontDoor.name,
            endpoint_name=endpointName,
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._frontend_endpoint, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
