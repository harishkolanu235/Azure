"""
Python Azure Script
"""
import os
import traceback
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient


GROUP_NAME = 'TCG-GROUP-PROD'


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id



def run_example():
    """Virtual Machine management example."""
    #
    # Create all clients with an Application (service principal) token provider
    #
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)


    # Delete Resource group and everything in it
    print("\nDeleting Resource Group {}".format(GROUP_NAME))
    delete_async_operation = resource_client.resource_groups.delete(
        GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))


if __name__ == "__main__":
    run_example()













