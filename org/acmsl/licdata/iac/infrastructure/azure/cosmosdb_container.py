# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/cosmosdb_container.py

This script defines the Azure CosmosDB Container for Licdata.

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
from typing import Dict, List


class CosmosdbContainer(BaseObject):
    """
    Azure CosmosDB Container for Licdata.

    Class name: CosmosdbContainer

    Responsibilities:
        - Define the Azure CosmosDB Container for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount,
        cosmosdbDatabase: pulumi_azure_native.documentdb.SqlResourceSqlDatabase,
    ):
        """
        Creates a new Azure instance.
        :param resourceGroup: The ResourceGroup.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param cosmosdbAccount: The CosmosDB account.
        :type cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount
        :param cosmosdbDatabase: The CosmosDB database.
        :param cosmosdbDatabase: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        """
        super().__init__()
        self._cosmosdb_container = self.create_cosmosdb_container(
            "licenses",
            cosmosdbAccount,
            cosmosdbDatabase,
            resourceGroup,
            {
                "paths": ["/id"],
                "kind": "Hash",
            },
        )
        self._cosmosdb_container.name.apply(
            lambda name: pulumi.export("cosmosdb_container", name)
        )

    @property
    def cosmosdb_container(
        self,
    ) -> pulumi_azure_native.documentdb.SqlResourceSqlContainer:
        """
        Retrieves the Cosmos DB Container.
        :return: Such container.
        :rtype: pulumi_azure_native.documentdb.SqlResourceSqlContainer
        """
        return self._cosmosdb_container

    def create_cosmosdb_container(
        self,
        containerName: str,
        cosmosDbAccount: pulumi_azure_native.documentdb.DatabaseAccount,
        cosmosDbDatabase: pulumi_azure_native.documentdb.SqlResourceSqlDatabase,
        resourceGroup: pulumi_azure_native.resources.ResourceGroup,
        partitionKey: Dict,
    ) -> pulumi_azure_native.documentdb.SqlResourceSqlContainer:
        """
        Creates an Azure Cosmos DB Container.
        :param containerName: The name of the container.
        :type containerName: str
        :param cosmosDbAccount: The Azure CosmosDB Account.
        :type cosmosDbAccount: pulumi_azure_native.documentdb.DatabaseAccount
        :param database: The Azure CosmosDB database.
        :type database: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        :param resourceGroup: The resource group.
        :type resourceGroup: pulumi_azure_native.resources.ResourceGroup
        :param partitionKey: The partition key.
        :type partitionKey: Dict
        :return: The Azure Cosmos DB Container.
        :rtype: pulumi_azure_native.documentdb.SqlResourceSqlContainer
        """
        return pulumi_azure_native.documentdb.SqlResourceSqlContainer(
            containerName,
            resource_group_name=resourceGroup.name,
            account_name=cosmosDbAccount.name,
            container_name=containerName,
            database_name=cosmosDbDatabase.name,
            location=resourceGroup.location,
            resource=pulumi_azure_native.documentdb.SqlContainerResourceArgs(
                id=cosmosDbDatabase.name, partition_key=partitionKey
            ),
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._cosmosdb_container, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
