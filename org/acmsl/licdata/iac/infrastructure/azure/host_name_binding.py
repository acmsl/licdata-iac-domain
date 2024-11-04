# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/host_name_binding.py

This script defines the HostNameBinding class.

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


class HostNameBinding:
    """
    A host name binding in Azure.

    Class name: HostNameBinding

    Responsibilities:
        - Declares an Azure host name binding.

    Collaborators:
        - None
    """

    def __init__(
        self,
        dnsRecord: pulumi_azure_native.network.RecordSet,
        functionApp: pulumi_azure_native.web.WebApp,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ):
        """
        Creates a new HostNameBinding instance.
        :param dnsRecord: The DNS record to bind.
        :type dnsRecord: pulumi_azure_native.network.RecordSet
        :param functionApp: The function app.
        :type functionApp: pulumi_azure_native.web.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._host_name_binding = self.create_host_name_binding(
            dnsRecord, functionApp, resourceGroup
        )
        self._host_name_binding.name.apply(
            lambda name: pulumi.export("host_name_binding", name)
        )

    @property
    def host_name_binding(self) -> pulumi_azure_native.web.HostNameBinding:
        """
        Retrieves the host name binding.
        :return: Such host name binding.
        :rtype: pulumi_azure_native.web.HostNameBinding
        """
        return self._host_name_binding

    def create_host_name_binding(
        self,
        dnsRecord: pulumi_azure_native.network.RecordSet,
        functionApp: pulumi_azure_native.web.WebApp,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.web.HostNameBinding:
        """
        Creates a new HostNameBinding instance.
        :param dnsRecord: The DNS record to bind.
        :type dnsRecord: pulumi_azure_native.network.RecordSet
        :param functionApp: The function app.
        :type functionApp: pulumi_azure_native.web.WebApp
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The blob container.
        :rtype: pulumi_azure_native.storage.BlobContainer
        """
        return pulumi_azure_native.web.HostNameBinding(
            dnsRecord.name.apply(lambda name: name),
            name=dnsRecord.name,
            site_name=functionApp.name,
            host_name_type="Verified",
            resource_group_name=resourceGroup.name,
            custom_host_name_binding_args=pulumi_azure_native.web.HostNameBindingArgs(
                custom_host_name=custom_hostname
            ),
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._host_name_binding, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
