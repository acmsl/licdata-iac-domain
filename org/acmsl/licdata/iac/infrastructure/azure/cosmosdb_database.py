# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/cosmosdb_database.py

This script defines the Azure CosmosDB Database for Licdata.

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
# Import Pulumi Azure SDK
import pulumi
import pulumi_azure_native
from typing import Dict, List


class CosmosdbDatabase:
    """
    Azure CosmosDB Database for Licdata.

    Class name: CosmosdbDatabase

    Responsibilities:
        - Define the Azure CosmosDB Database for Licdata.

    Collaborators:
        - None
    """

    def __init__(self, cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount):
        """
        Creates a new Azure instance.
        :param cosmosdbAccount: The CosmosDB account.
        :type cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount
        """
        super().__init__()
        self._cosmosdb_database = self.create_cosmosdb_database(
            "licenses", cosmosdbAccount
        )
        self._cosmosdb_database.name.apply(
            lambda name: pulumi.export("cosmosdb_database", name)
        )

    @property
    def cosmosdb_database(
        self,
    ) -> pulumi_azure_native.documentdb.SqlResourceSqlDatabase:
        """
        Retrieves the Cosmos DB Database.
        :return: Such database.
        :rtype: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        """
        return self._cosmosdb_database

    def create_cosmosdb_database(
        self,
        databaseName: str,
        cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount,
    ) -> pulumi_azure_native.documentdb.SqlResourceSqlDatabase:
        """
        Creates an Azure Cosmos DB Database.
        :param databaseName: The name of the database.
        :type databaseName: str
        :param cosmosdbAccount: The Azure Cosmos DB Account.
        :type cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount
        :return: The Azure Cosmos DB Database.
        :rtype: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        """
        return pulumi_azure_native.documentdb.SqlResourceSqlDatabase(
            databaseName,
            resource_group_name=cosmosdbAccount.resource_group_name,
            account_name=cosmosdbAccount.name,
            resource={
                "id": databaseName,
            },
        )

    def __getattr__(self, attr):
        """
        Delegates attribute/method lookup to the wrapped instance.
        :param attr: The attribute.
        :type attr: Any
        """
        return getattr(self._cosmosdb_database, attr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
