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
# Import Pulumi Azure SDK
import pulumi
import pulumi_azure_native
from pulumi_azure_native import apimanagement, resources, storage, web, sql, network
from typing import Dict, List


class CosmosdbAccount:
    """
    Azure CosmosDB Account for Licdata.

    Class name: CosmosdbAccount

    Responsibilities:
        - Define the Azure CosmosDB Account for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, resourceGroup: pulumi_azure_native.resources.ResourceGroup):
        """
        Creates a new Azure instance.
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        """
        super().__init__()
        self._cosmosdb_account = self.create_cosmosdb_account(
            "cosmosdb",
            "GlobalDocumentDB",
            "Standard",
            {
                "defaultConsistencyLevel": "Session",
            },
            self._resource_group,
        )
        self._cosmosdb_account.name.apply(
            lambda name: pulumi.export("cosmosdb_account", name)
        )

    @property
    def cosmosdb_account(self) -> pulumi_azure_native.documentdb.DatabaseAccount:
        """
        Retrieves the Cosmos DB Account.
        :return: Such account.
        :rtype: pulumi_azure_native.documentdb.DatabaseAccount
        """
        return self._cosmosdb_account

    def create_cosmosdb_account(
        self,
        accountName: str,
        kind: str,
        databaseAccountOfferType: str,
        consistencyPolicy: Dict[str, str],
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
    ) -> pulumi_azure_native.documentdb.DatabaseAccount:
        """
        Creates an Azure Cosmos DB Account.
        :param accountName: The name of the account.
        :type accountName: str
        :param offerType: The offer type.
        :type offerType: str
        :param kind: The kind of account.
        :type kind: str
        :param databaseAccountOfferType: The database account offer type.
        :type databaseAccountOfferType: str
        :param consistencyPolicy: The consistency policy.
        :type consistencyPolicy: Dict[str,str]
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :return: The Azure Cosmos DB Account.
        :rtype: pulumi_azure_native.documentdb.DatabaseAccount
        """
        return pulumi_azure_native.documentdb.DatabaseAccount(
            accountName,
            resource_group_name=resourceGroup.name,
            location=resourceGroup.location,
            kind=kind,
            database_account_offer_type=databaseAccountOfferType,
            consistency_policy=consistencyPolicy,
            locations=[
                pulumi_azure_native.documentdb.LocationArgs(
                    location_name=resourceGroup.location, failover_priority=0
                )
            ],
            enable_free_tier=True,  # Use free tier for cost-effective setup
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._api_service_plan, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
