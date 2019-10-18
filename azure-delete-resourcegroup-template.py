"""
Microsoft Azure Python Script - Resource Deletion Example
Mickal Speller for THATCLIGUY.com
Sept 2019, version 1.0

Note: Script is free to use without any warranty and/or support from Mickal Speller (thatcliguy.com).
For full and complete details, please reference Microsoft Azure website for full details and usage for the Azure Python API
"""

import os
import traceback
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

    # Specify the Resource Group to Delete
GROUP_NAME = 'TCG-GROUP-PROD'

def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

def run_example():    #
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)

    # Delete Entire Resource Group
    print("\nDeleting Resource Group {}".format(GROUP_NAME))
    delete_async_operation = resource_client.resource_groups.delete(
        GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))

if __name__ == "__main__":
    run_example()













