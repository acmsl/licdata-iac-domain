# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/web_app_host_name_binding.py

This script defines the WebAppHostNameBinding class.

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
from .dns_record import DnsRecord
from .web_app import WebApp
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class WebAppHostNameBinding(AzureResource):
    """
    A web-app host name binding in Azure.

    Class name: WebAppHostNameBinding

    Responsibilities:
        - Declares an Azure WebApp host name binding.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        hostNameType: str,
        customHostName: str,
        dnsRecord: DnsRecord,
        webApp: WebApp,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new WebAppHostNameBinding instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param hostNameType: The host name type.
        :type hostNameType: str
        :param customHostName: The custom host name.
        :type customHostName: str
        :param dnsRecord: The DNS record to bind.
        :type dnsRecord: org.acmsl.licdata.iac.infrastructure.azure.DnsRecord
        :param webApp: The function app.
        :type webApp: org.acmsl.licdata.iac.infrastructure.azure.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.iac.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {
                "dns_record": dnsRecord,
                "web_app": webApp,
                "resource_group": resourceGroup,
            },
        )
        self._host_name_type = hostNameType
        self._custom_host_name = customHostName

    @property
    def host_name_type(self) -> str:
        """
        Retrieves the host name type.
        :return: Such type.
        :rtype: str
        """
        return self._host_name_type if self._host_name_type is not None else "Verified"

    @property
    def custom_host_name(self) -> str:
        """
        Retrieves the custom host name.
        :return: Such name.
        :rtype: str
        """
        return self._custom_host_name

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
        return "wahnb"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.web.WebAppHostNameBinding:
        """
        Creates a new HostNameBinding instance.
        :param name: The name.
        :type name: str
        :return: The binding.
        :rtype: pulumi_azure_native.web.WebAppHostNameBinding
        """
        return pulumi_azure_native.web.WebAppHostNameBinding(
            name,
            name=self.dns_record.name,
            site_name=self.web_app.name,
            host_name_type=self.host_name_type,
            resource_group_name=self.resource_group.name,
            custom_host_name_binding_args=pulumi_azure_native.web.HostNameBindingArgs(
                custom_host_name=self.custom_hostname
            ),
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.web.WebAppHostNameBinding):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.web.WebAppHostNameBinding
        """
        resource.name.apply(lambda name: pulumi.export("host_name_binding", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
