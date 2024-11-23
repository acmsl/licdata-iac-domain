# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/app_service_plan.py

This script defines the AppServicePlan class.

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


class AppServicePlan(AzureResource):
    """
    Azure App Service Plan for Licdata.

    Class name: AppServicePlan

    Responsibilities:
        - Define the Azure App Service Plan for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        kind: str,
        tierType: str,
        tierName: str,
        capacity: int,
        targetWorkerCount: int,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new AppServicePlan instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param kind: The type of app service plan.
        :type kind: str
        :param tierType: The tier type.
        :type tierType: str
        :param tierName: The name of the tier.
        :type tierName: str
        :param capacity: The capacity.
        :type capacity: int
        :param targetWorkerCount: The number of workers.
        :type targetWorkerCount: int
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: org.acmsl.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._kind = kind
        self._tier_type = tierType
        self._tier_name = tierName
        self._capacity = capacity
        self._target_worker_count = targetWorkerCount

    @property
    def kind(self) -> str:
        """
        Retrieves the kind of app service plan.
        :return: Such kind.
        :rtype: str
        """
        return self._kind if self._kind is not None else "FunctionApp"

    @property
    def tier_type(self) -> str:
        """
        Retrieves the tier type.
        :return: Such type.
        :rtype: str
        """
        return self._tier_type if self._tier_name is not None else "Dynamic"

    @property
    def tier_name(self) -> str:
        """
        Retrieves the tier name.
        :return: Such name.
        :rtype: str
        """
        return self._tier_name if self._tier_name is not None else "S1"

    @property
    def capacity(self) -> int:
        """
        Retrieves the capacity.
        :return: Such value.
        :rtype: int
        """
        return self._capacity if self._capacity is not None else 1

    @property
    def target_worker_count(self) -> int:
        """
        Retrieves the target worker count.
        :return: Such count.
        :rtype: int
        """
        return self._target_worker_count if self._target_worker_count is not None else 1

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
        return "appsp"

    # @override
    def _create(self, name: str) -> pulumi_azure_native.web.AppServicePlan:
        """
        Creates the resource.
        :param name: The name of the resource.
        :type name: str
        :return: The Azure App Service Plan.
        :rtype: pulumi_azure_native.web.AppServicePlan
        """
        return pulumi_azure_native.web.AppServicePlan(
            name,
            resource_group_name=self.resource_group.name,
            kind=self.kind,
            sku=pulumi_azure_native.web.SkuDescriptionArgs(
                tier=self.tier_type, name=self.tier_name, capacity=self.capacity
            ),
            location=self.location,
            reserved=True,
            target_worker_count=self.target_worker_count,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.web.AppServicePlan):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.web.AppServicePlan
        """
        resource.name.apply(lambda name: pulumi.export("app_service_plan", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
