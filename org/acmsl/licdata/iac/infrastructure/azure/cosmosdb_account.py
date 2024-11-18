# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/cosmosdb_account.py

This script defines the Azure CosmosDB Account for Licdata.

Copyright (C) 2024-today acmsl's licdata-iac

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
from org.acmsl.licdata.iac.domain import Resource
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native
from pulumi_azure_native import apimanagement, resources, storage, web, sql, network
from typing import override


class CosmosdbAccount(Resource):
    """
    Azure CosmosDB Account for Licdata.

    Class name: CosmosdbAccount

    Responsibilities:
        - Define the Azure CosmosDB Account for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        offerType: str,
        kind: str,
        consistencyPolicy: Dict[str, str],
        enableFreeTier: bool,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Azure instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param offerType: The offer type.
        :type offerType: str
        :param kind: The kind of account.
        :type kind: str
        :param consistencyPolicy: The consistency policy.
        :type consistencyPolicy: Dict[str,str]
        :param enableFreeTier: Whether to enable free tier.
        :type enableFreeTier: bool
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__(
            stackName, projectName, location, {"resource_group": resourceGroup}
        )
        self._kind = kind
        self._offer_type = offerType
        self._consistency_policy = consistencyPolicy
        self._enable_free_tier = enableFreeTier

    @property
    def kind(self) -> str:
        """
        Retrieves the kind.
        :return: The kind.
        :rtype: str
        """
        return self._kind if self._kind is not None else "GlobalDocumentDB"

    @property
    def offer_type(self) -> str:
        """
        Retrieves the offer type.
        :return: The offer type.
        :rtype: str
        """
        return self._offer_type if self._offer_type is not None else "Standard"

    @property
    def consistency_policy(self) -> Dict[str, str]:
        """
        Retrieves the consistency policy.
        :return: The consistency policy.
        :rtype: Dict[str,str]
        """
        return (
            (
                self._consistency_policy
                if self._consistency_policy
                else {"defaultConsistencyLevel": "Session"}
            ),
        )

    @property
    def enable_free_tier(self) -> bool:
        """
        Retrieves whether to enable free tier.
        :return: Whether to enable free tier.
        :rtype: bool
        """
        return self._enable_free_tier if self._enable_free_tier is not None else True

    # @override
    def _create(self, name: str) -> Any:
        """
        Creates an Azure Cosmos DB Account.
        :param name: The name of the resource.
        :type name: str
        :return: The Azure Cosmos DB Account.
        :rtype: pulumi_azure_native.documentdb.DatabaseAccount
        """
        return pulumi_azure_native.documentdb.DatabaseAccount(
            name,
            resource_group_name=self.resource_group.name,
            location=self.resource_group.location,
            kind=self.kind,
            database_account_offer_type=self.offer_type,
            consistency_policy=self.consistency_policy,
            locations=[
                pulumi_azure_native.documentdb.LocationArgs(
                    location_name=self.location, failover_priority=0
                )
            ],
            enable_free_tier=self.enable_free_tier,
        )

    # @override
    def _post_create(self, resource: pulumi_azure_native.documentdb.DatabaseAccount):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.documentdb.DatabaseAccount
        """
        resource.name.apply(lambda name: pulumi.export("cosmosdb_account", name))

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._api_service_plan, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
