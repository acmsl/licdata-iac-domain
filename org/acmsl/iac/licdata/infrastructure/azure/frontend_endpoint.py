# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/frontend_endpoint.py

This script defines the FrontendEndpoint class.

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
from .dns_record import DnsRecord
from .dns_zone import DnsZone
from .front_door import FrontDoor
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class FrontendEndpoint(AzureResource):
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
        stackName: str,
        projectName: str,
        location: str,
        endpointName: str,
        frontDoor: FrontDoor,
        dnsRecord: DnsRecord,
        dnsZone: DnsZone,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Frontend Endpoint.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param endpointName: The name of the endpoint.
        :type endpointName: str
        :param frontDoor: The Front Door.
        :type frontDoor: pulumi_azure_native.cdn.Profile
        :param dnsRecord: The DNS record for the endpoint.
        :type dnsRecord: org.acmsl.iac.licdata.infrastructure.azure.DnsRecord
        :param dnsZone: The DNS zone.
        :type dnsZone: org.acmsl.iac.licdata.infrastructure.azure.DnsZone
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "front_door": frontDoor,
                "dns_record": dnsRecord,
                "dns_zone": dnsZone,
                "resource_group": resourceGroup,
            },
        )
        self._endpoint_name = endpointName

        self._frontend_endpoint = self.create_frontend_endpoint(
            "license", "licenseEndpoint", frontDoor, dnsRecord, dnsZone, resourceGroup
        )

    @property
    def endpoint_name(self) -> str:
        """
        Retrieves the endpoint name.
        :return: The endpoint name.
        :rtype: str
        """
        return self._endpoint_name if self._endpoint_name is not None else "licdata"

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
        return "fe"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.cdn.AFDEndpoint:
        """
        Creates a Front Door.
        :param name: The name of the frontend endpoint.
        :type name: str
        :return: The FrontendEndpoint instance.
        :rtype: pulumi_azure_native.cdn.AFDEndpoint
        """
        # Construct the FQDN using the record set name and the DNS zone name
        fqdn = pulumi.Output.concat(self.dns_record.name, ".", self.dns_zone.name)

        return pulumi_azure_native.cdn.AFDEndpoint(
            name,
            resource_group_name=self.resource_group.name,
            profile_name=self.front_door.name,
            endpoint_name=self.endpoint_name,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.cdn.AFDEndpoint):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.cdn.AFDEndpoint
        """
        resource.name.apply(lambda name: pulumi.export("frontend_endpoint", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
