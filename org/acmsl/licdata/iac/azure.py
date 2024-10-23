# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/azure.py

This script defines the Azure class.

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
import pulumi_azure_native as azure_native
import pulumi_azure as azure
from pulumi_azure_native import resources, storage, web, sql, network
from pulumi_azure_native import apimanagement
from typing import Dict


class Azure:
    """
    IaC implementation for Azure.

    Class name: Azure

    Responsibilities:
        - Define the infrastructure for the Azure cloud provider.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new Azure instance.
        """
        super().__init__()
        self._resource_group = self.create_resource_group("licenses")
        self._cosmosdb_account = self.create_cosmosdb_account(
            "cosmosdb",
            "Standard",
            "GlobalDocumentDB",
            "Standard",
            {
                "defaultConsistencyLevel": "Session",
            },
            self._resource_group,
        )
        self._cosmosdb_database = self.create_cosmosdb_database(
            "licenses", self._cosmosdb_account
        )
        self._cosmosdb_container = self.create_cosmosdb_container(
            "licenses",
            self._cosmosdb_account,
            self._cosmosdb_database,
            {
                "paths": ["/id"],
                "kind": "Hash",
            },
        )
        self._storage_account = self.create_storage_account(
            self._resource_group, "licenses", "StorageV2"
        )
        self._sessions_table = self.create_table(
            "sessions", self._storage_account, self._resource_group
        )
        self._app_service_plan = self.create_app_service_plan(
            "licenses", self._resource_group
        )
        self._function_app = self.create_function_app(
            "licenses", self._app_service_plan, self._storage_account
        )
        self._function_storage_account = self.create_storage_account(
            self._resource_group, "functionStorage", "StorageV2"
        )
        self._api_management_service = self.create_api_managenent_service(
            "licenses",
            self.resource_group,
            "admin@example.com",
            "admin",
            "Consumption",
            0,
        )
        self._api = self.create_api(
            "licensesApi",
            self._resource_group,
            self._api_management_service,
            "licenses",
            "Licenses API",
        )
        self._public_ip = self.create_public_ip_address(
            "licenses", self._resource_group
        )
        self._dns_zone = self.create_dns_zone(
            "licenses", "licenses.acmsl.org", self._resource_group
        )
        self._ar_record = self.create_arrecord(
            "apiDns",
            self._dns_zone,
            self._resource_group,
            300,
            [self._public_ip.ip_address],
        )
        self._security_group = self.create_network_security_group(
            "functionSecurityGroup",
            self._resource_group,
            self.create_security_rule_args_for_accessing_cosmosdb(),
        )

    @property
    def resource_group(self) -> azure_native.resources.ResourceGroup:
        """
        Retrieves the Azure Resource Group.
        :return: Such Resource Group.
        :rtype: azure_native.resources.ResourceGroup
        """
        return self._resource_group

    @property
    def cosmosdb_account(self) -> azure_native.documentdb.DatabaseAccount:
        """
        Retrieves the Cosmos DB Account.
        :return: Such account.
        :rtype: azure_native.documentdb.DatabaseAccount
        """
        return self._cosmosdb_account

    @property
    def cosmosdb_database(self) -> azure_native.documentdb.SqlDatabase:
        """
        Retrieves the Cosmos DB Database.
        :return: Such database.
        :rtype: azure_native.documentdb.SqlDatabase
        """
        return self._cosmosdb_database

    @property
    def cosmosdb_container(self) -> azure.documentdb.SqlContainer:
        """
        Retrieves the Cosmos DB Container.
        :return: Such container.
        :rtype: azure.documentdb.SqlContainer
        """
        return self._cosmosdb_container

    @property
    def storage_account(self) -> azure_native.storage.StorageAccount:
        """
        Retrieves the storage account.
        :return: Such storage account.
        :rtype: azure_native.storage.StorageAccount
        """
        return self._storage_account

    @property
    def sessions_table(self) -> azure_native.storage.Table:
        """
        Retrieves the sessions table.
        :return: Such table.
        :rtype: azure_native.storage.Table
        """
        return self._sessions_table

    @property
    def app_service_plan(self) -> azure_native.web.AppServicePlan:
        """
        Retrieves the App Service Plan.
        :return: Such App Service Plan.
        :rtype: azure_native.web.AppServicePlan
        """
        return self._app_service_plan

    @property
    def function_storage_account(self) -> azure_native.storage.StorageAccount:
        """
        Retrieves the function storage account.
        :return: Such storage account.
        :rtype: azure_native.storage.StorageAccount
        """
        return self._function_storage_account

    @property
    def api_management_service(self) -> apimanagement.Service:
        """
        Retrieves the API Management Service.
        :return: Such API Management Service.
        :rtype: apimanagement.Service
        """
        return self._api_management_service

    @property
    def api(self) -> apimanagement.Api:
        """
        Retrieves the API.
        :return: Such API.
        :rtype: apimanagement.Api
        """
        return self._api

    @property
    def public_ip(self) -> azure_native.network.PublicIPAddress:
        """
        Retrieves the public IP address.
        :return: Such public IP address.
        :rtype: azure_native.network.PublicIPAddress
        """
        return self._public_ip

    @property
    def dns_zone(self) -> azure_native.dns.Zone:
        """
        Retrieves the DNS zone.
        :return: Such DNS zone.
        :rtype: azure_native.dns.Zone
        """
        return self._dns_zone

    @property
    def ar_record(self) -> azure_native.dns.ARecord:
        """
        Retrieves the A record.
        :return: Such A record.
        :rtype: azure_native.dns.ARecord
        """
        return self._ar_record

    @property
    def security_group(self) -> network.NetworkSecurityGroup:
        """
        Retrieves the security group.
        :return: Such security group.
        :rtype: network.NetworkSecurityGroup
        """
        return self._security_group

    def create_resource_group(
        self, resourceGroupName: str
    ) -> azure_native.resources.ResourceGroup:
        """
        Creates an Azure Resource Group.
        :param resourceGroupName: The name of the resource group.
        :type resourceGroupName: str
        :return: The Azure Resource Group.
        :rtype: azure_native.resources.ResourceGroup
        """
        return azure_native.resources.ResourceGroup(resourceGroupName)

    def create_cosmosdb_account(
        self,
        accountName: str,
        offerType: str,
        kind: str,
        databaseAccountOfferType: str,
        consistencyPolicy: Dict[str, str],
        resourceGroup: azure_native.resources.ResourceGroup,
    ) -> azure_native.documentdb.DatabaseAccount:
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
        :type resourceGroup: azure_native.resources.ResourceGroup
        :return: The Azure Cosmos DB Account.
        :rtype: azure_native.documentdb.DatabaseAccount
        """
        return azure_native.documentdb.DatabaseAccount(
            accountName,
            resource_group_name=resourceGroup.name,
            location=resourceGroup.location,
            offer_type=offerType,
            kind=kind,
            database_account_offer_type=databaseAccountOfferType,
            consistency_policy=consistencyPolicy,
            enable_free_tier=True,  # Use free tier for cost-effective setup
        )

    def create_cosmosdb_database(
        self,
        databaseName: str,
        cosmosdbAccount: azure_native.documentdb.DatabaseAccount,
    ) -> azure_native.documentdb.SqlDatabase:
        """
        Creates an Azure Cosmos DB Database.
        :param databaseName: The name of the database.
        :type databaseName: str
        :param cosmosdbAccount: The Azure Cosmos DB Account.
        :type cosmosdbAccount: azure_native.documentdb.DatabaseAccount
        :return: The Azure Cosmos DB Database.
        :rtype: azure_native.documentdb.SqlDatabase
        """
        return azure_native.documentdb.SqlDatabase(
            databaseName,
            resource_group_name=cosmosdbAccount.resource_group_name,
            account_name=cosmosdbAccount.name,
            resource={
                "id": databaseName,
            },
        )

    def create_cosmosdb_container(
        self,
        containerName: str,
        cosmosDbAccount: azure_native.documentdb.DatabaseAccount,
        databaseName: str,
        resourceName: str,
        partitionKey: Dict,
    ) -> azure.documentdb.SqlContainer:
        """
        Creates an Azure Cosmos DB Container.
        :param containerName: The name of the container.
        :type containerName: str
        :param cosmosDbAccount: The Azure Cosmos DB Account.
        :type cosmosDbAccount: azure_native.documentdb.DatabaseAccount
        :param databaseName: The name of the database.
        :type databaseName: str
        :param resourceName: The name of the resource.
        :type resourceName: str
        :param partitionKey: The partition key.
        :type partitionKey: Dict
        :return: The Azure Cosmos DB Container.
        :rtype: azure.documentdb.SqlContainer
        """
        return azure.documentdb.SqlContainer(
            containerName,
            resource_group_name=cosmosDbAccount.resource_group_name,
            account_name=cosmosDbAccount.name,
            database_name=databaseName,
            resource={"id": databaseName, "partitionKey": partitionKey},
        )

    def create_storage_account(
        self,
        accountName: str,
        resourceGroup: azure_native.resources.ResourceGroup,
        kind: str,
    ) -> azure_native.storage.StorageAccount:
        """
        Creates an Azure Storage Account.
        :param accountName: The name of the account.
        :type accountName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :param kind: The kind of account.
        :type kind: str
        :return: The Azure Storage Account.
        :rtype: azure_native.storage.StorageAccount
        """
        return azure_native.storage.StorageAccount(
            accountName,
            resource_group_name=resourceGroup.name,
            location=resourceGroup.location,
            sku=azure_native.storage.SkuArgs(name="Standard_LRS"),
            kind=kind,
        )

    def create_table(
        self,
        tableName: str,
        storageAccount: azure_native.storage.StorageAccount,
        resourceGroup: azure_native.resources.ResourceGroup,
    ) -> azure_native.storage.Table:
        """
        Creates a new table.
        :param tableName: The name of the table.
        :type tableName: str
        :param storageAccount: The storage account.
        :type storageAccount: azure_native.storage.StorageAccount
        :param resourceGroup: The resource group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :return: The table.
        :rtype: azure_native.storage.Table
        """

        return azure_native.storage.Table(
            tableName,
            storage_account_name=storageAccount.name,
            name=tableName,
            resource_group_name=resourceGroup.name,
        )

    def create_app_service_plan(
        self,
        appServicePlanName: str,
        resourceGroup: azure_native.resources.ResourceGroup,
    ) -> azure_native.web.AppServicePlan:
        """
        Creates an Azure App Service Plan.
        :param appServicePlanName: The name of the App Service Plan.
        :type appServicePlanName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :return: The Azure App Service Plan.
        :rtype: azure_native.web.AppServicePlan
        """
        return azure_native.web.AppServicePlan(
            appServicePlanName,
            resource_group_name=resourceGroup.name,
            kind="FunctionApp",
            sku=web.SkuDescriptionArgs(tier="Dynamic", name="Y1"),
        )

    def create_function_app(
        self,
        functionName: str,
        appServicePlan: azure_native.web.AppServicePlan,
        functionStorageAccount: azure_native.storage.StorageAccount,
    ) -> azure_native.web.WebApp:
        """
        Creates an Azure Function App.
        :param functionName: The name of the function.
        :type functionName: str
        :param appServicePlan: The App Service Plan.
        :type appServicePlan: azure_native.web.AppServicePlan
        :param functionStorageAccount: The Storage Account.
        :type functionStorageAccount: azure_native.storage.StorageAccount
        :return: The Azure Function App.
        :rtype: azure_native.web.WebApp
        """
        return azure_native.web.WebApp(
            functionName,
            resource_group_name=appServicePlan.resource_group_name,
            server_farm_id=appServicePlan.id,
            kind="FunctionApp",
            site_config=azure_native.web.SiteConfigArgs(
                app_settings=[
                    azure_native.web.NameValuePairArgs(
                        name="AzureWebJobsStorage",
                        value=functionStorageAccount.primary_connection_string,
                    ),
                    azure_native.web.NameValuePairArgs(
                        name="FUNCTIONS_EXTENSION_VERSION", value="~4"
                    ),
                    azure_native.web.NameValuePairArgs(
                        name="WEBSITE_RUN_FROM_PACKAGE", value="1"
                    ),
                ]
            ),
            https_only=True,
        )

    def create_api_managenent_service(
        self,
        serviceName: str,
        resourceGroup: azure_native.resources.ResourceGroup,
        publisherName: str,
        publisherEmail: str,
        skuName: str,
        skuCapacity: int,
    ) -> apimanagement.Service:
        """
        Creates an API Management Service.
        :param serviceName: The name of the service.
        :type serviceName: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :param publisherName: The name of the publisher.
        :type publisherName: str
        :param publisherEmail: The email of the publisher.
        :type publisherEmail: str
        :param skuName: The name of the SKU.
        :type skuName: str
        :param skuCapacity: The capacity of the SKU.
        :type skuCapacity: int
        :return: The API Management Service.
        :rtype: apimanagement.Service
        """
        return apimanagement.Service(
            serviceName,
            resource_group_name=resourceGroup.name,
            publisher_email=publisherEmail,
            publisher_name=publisherName,
            sku=apimanagement.SkuPropertiesArgs(
                name=skuName,
                capacity=skuCapacity,
            ),
        )

    def create_api(
        self,
        name: str,
        resourceGroup: azure_native.resources.ResourceGroup,
        apiManagementService: apimanagement.Service,
        path: str,
        displayName: str,
    ) -> apimanagement.Api:
        """
        Creates an API.
        :param name: The name of the API.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :param apiManagementService: The API Management Service.
        :type apiManagementService: apimanagement.Service
        :param path: The path of the API.
        :type path: str
        :param displayName: The display name of the API.
        :type displayName: str
        :return: The API.
        :rtype: apimanagement.Api
        """
        return apimanagement.Api(
            name,
            resource_group_name=resourceGroup.name,
            service_name=apiManagementService.name,
            path=path,
            protocols=["https"],
            display_name=displayName,
        )

    def create_public_ip_address(
        self, name: str, resourceGroup: azure_native.resources.ResourceGroup
    ) -> azure_native.network.PublicIPAddress:
        """
        Creates a public IP address.
        :param name: The name of the public IP address.
        :type name: str
        :param resourceGroup: The Azure Resource Group.
        :type resourceGroup: azure_native.resources.ResourceGroup
        :return: The public IP address.
        :rtype: azure_native.network.PublicIPAddress
        """
        return azure_native.network.PublicIPAddress(
            name,
            resource_group_name=resourceGroup.name,
            public_ip_allocation_method="Static",
        )

    def create_dns_zone(
        self,
        name: str,
        domainName: str,
        resource_group: azure_native.resources.ResourceGroup,
    ) -> azure_native.dns.Zone:
        """
        Creates a DNS zone.
        :param name: The name of the DNS zone.
        :type name: str
        :param domainName: The domain name.
        :type domainName: str
        :param resource_group: The Azure Resource Group.
        :type resource_group: azure_native.resources.ResourceGroup
        :return: The DNS zone.
        :rtype: azure_native.dns.Zone
        """
        return azure_native.dns.Zone(
            name,
            resource_group_name=resourceGroup.name,
            zone_type="Public",
            name=domainName,
        )

    def create_arrecord(
        self,
        name: str,
        dnsZone: azure_native.dns.Zone,
        resource_group: azure_native.resources.ResourceGroup,
        ttl: int,
        records: List[str],
    ) -> azure_native.dns.ARecord:
        """
        Creates an A record.
        :param name: The name of the A record.
        :type name: str
        :param dnsZone: The DNS zone.
        :type dnsZone: azure_native.dns.Zone
        :param resource_group: The resource group.
        :type resource_group: azure_native.resources.ResourceGroup
        :param ttl: The TTL.
        :type ttl: int
        :param records: The records.
        :type records: List[str]
        :return: The A record.
        :rtype: azure_native.dns.ARecord
        """
        return azure_native.dns.ARecord(
            name,
            zone_name=dnsZone.name,
            resource_group_name=resourceGroup.name,
            ttl=ttl,
            records=records,
        )

    def create_security_rule_args_for_accessing_cosmosdb(
        self,
    ) -> network.SecurityRuleArgs:
        """
        Creates a security rule args for accessing CosmosDB.
        :return: The security rule.
        :rtype: network.SecurityRule
        """
        return network.SecurityRuleArgs(
            name="AllowFunctionsToCosmosDB",
            priority=100,
            direction="Inbound",
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range="443",
            source_address_prefix="*",
            destination_address_prefix="CosmosDB",
        )

    def create_network_security_group(
        self,
        name: str,
        resourceGroup: azure_native.resources.ResourceGroup,
        securityRuleArgs: List[network.SecurityRuleArgs],
    ) -> network.NetworkSecurityGroup:
        return network.NetworkSecurityGroup(
            name,
            resource_group_name=resourceGroup.name,
            security_rules=securityRuleArgs,
        )

    def deploy(self):
        """
        Deploys the infrastructure.
        """
        pulumi.export("resource_group", self.resource_group.name)
        pulumi.export("cosmosdb_account", self.cosmosdb_account.name)
        pulumi.export("cosmosdb_database", self.cosmosdb_database.name)
        pulumi.export("cosmosdb_container", self.cosmosdb_container.name)
        pulumi.export("storage_account", self.storage_account.name)
        pulumi.export("sessions_table", self.sessions_table.name)
        pulumi.export("app_service_plan", self.app_service_plan.name)
        pulumi.export("function_app", self.function_app.name)
        pulumi.export("function_storage_account", self.function_storage_account.name)
        pulumi.export("api_management_service", self.api_management_service.name)
        pulumi.export("api", self.api.name)
        pulumi.export("public_ip", self.public_ip.name)
        pulumi.export("dns_zone", self.dns_zone.name)
        pulumi.export("ar_record", self.ar_record.name)
        pulumi.export("security_group", self.security_group.name)
        pulumi.export("api_url", self.public_ip.ip_address)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
