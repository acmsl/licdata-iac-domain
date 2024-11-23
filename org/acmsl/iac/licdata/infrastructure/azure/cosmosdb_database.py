# vim: set fileencoding=utf-8
"""
org/acmsl/iac/licdata/infrastructure/azure/cosmosdb_database.py

This script defines the Azure CosmosDB Database for Licdata.

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
from .cosmosdb_account import CosmosdbAccount
from .resource_group import ResourceGroup
import pulumi
import pulumi_azure_native


class CosmosdbDatabase(AzureResource):
    """
    Azure CosmosDB Database for Licdata.

    Class name: CosmosdbDatabase

    Responsibilities:
        - Define the Azure CosmosDB Database for Licdata.

    Collaborators:
        - None
    """

    def __init__(
        self,
        stackName: str,
        projectName: str,
        location: str,
        cosmosdbAccount: CosmosdbAccount,
        resourceGroup: ResourceGroup,
    ):
        """
        Creates a new Azure CosmosDB database instance.
        :param stackName: The name of the stack.
        :type stackName: str
        :param projectName: The name of the project.
        :type projectName: str
        :param location: The Azure location.
        :type location: str
        :param cosmosdbAccount: The CosmosDB account.
        :type cosmosdbAccount: pulumi_azure_native.documentdb.DatabaseAccount
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: org.acmsl.iac.licdata.infrastructure.azure.ResourceGroup
        """
        super().__init__(
            stackName,
            projectName,
            location,
            {"cosmosdb_account": cosmosdb_account, "resource_group": resourceGroup},
        )

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
        return "cdb"

    # @override
    def _create(
        self, name: str
    ) -> pulumi_azure_native.documentdb.SqlResourceSqlDatabase:
        """
        Creates an Azure Cosmos DB Database.
        :param name: The name of the resource.
        :type name: str
        :return: The Azure Cosmos DB Database.
        :rtype: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        """
        return pulumi_azure_native.documentdb.SqlResourceSqlDatabase(
            name,
            resource_group_name=self.resource_group.name,
            account_name=self.cosmosdb_account.name,
            resource={
                "id": name,
            },
        )

    # @override
    def _post_create(
        self, resource: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
    ):
        """
        Post-create hook.
        :param resource: The resource.
        :type resource: pulumi_azure_native.documentdb.SqlResourceSqlDatabase
        """
        resource.name.apply(lambda name: pulumi.export("cosmosdb_database", name))


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
