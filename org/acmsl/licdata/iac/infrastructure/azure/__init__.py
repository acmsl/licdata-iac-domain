# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/iac/infrastructure/azure/__init__.py

This file ensures org.acmsl.licdata.iac.infrastructure.azure is a package.

Copyright (C) 2024-today acm-sl's licdata

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .resource_group import ResourceGroup
from .cosmosdb_account import CosmosdbAccount
from .cosmosdb_database import CosmosdbDatabase
from .cosmosdb_container import CosmosdbContainer
from .storage_account import StorageAccount
from .databases_storage_account import DatabasesStorageAccount
from .sessions_table import SessionsTable
from .app_service_plan import AppServicePlan
from .function_app import FunctionApp
from .function_storage_account import FunctionStorageAccount
from .api_management_service import ApiManagementService
from .api import Api
from .public_ip_address import PublicIpAddress
from .dns_zone import DnsZone
from .dns_record import DnsRecord
from .security_group import SecurityGroup
from .blob_container import BlobContainer
from .blob import Blob
from .functions_package import FunctionsPackage
from .front_door import FrontDoor
from .frontend_endpoint import FrontendEndpoint
from .web_app_deployment_slot import WebAppDeploymentSlot
from .functions_deployment_slot import FunctionsDeploymentSlot
from .pulumi_azure_stack import PulumiAzureStack
from .pulumi_azure_stack_factory import PulumiAzureStackFactory

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
