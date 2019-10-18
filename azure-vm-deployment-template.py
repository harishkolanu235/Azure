"""
Microsoft Azure Python Script - Resource Group Creation Example
Mickal Speller for THATCLIGUY.com
Sept 2019, version 1.0

Note: Script is free to use without any warranty and/or support from Mickal Speller (thatcliguy.com).
For full and complete details, please reference the Azure SDK for Python documentation from Microsoft at https://docs.microsoft.com/en-us/azure/python/
"""

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption

SUBSCRIPTION_ID = 'INPUT_YOUR_AZURE_SUBSCRIPTION_ID'
GROUP_NAME = 'INPUT_GROUP_NAME'
LOCATION = 'INPUT_LOCATION'
VM_NAME = 'INPUT_VM_NAME'

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id = 'INPUT_YOUR_AZURE_CLIENT_ID',
        secret = 'INPUT_YOUR_AZURE_SECRET',
        tenant = 'INPUT_YOUR_AZURE_TENANT_ID'
    )

    return credentials

def create_resource_group(resource_group_client):
    resource_group_params = { 'location':LOCATION }
    resource_group_result = resource_group_client.resource_groups.create_or_update(
        GROUP_NAME,
        resource_group_params
    )

def create_availability_set(compute_client):
    avset_params = {
        'location': LOCATION,
        'sku': { 'name': 'Aligned' },
        'platform_fault_domain_count': 3
    }
    availability_set_result = compute_client.availability_sets.create_or_update(
        GROUP_NAME,
        'myAVSet',
        avset_params
    )

def create_public_ip_address(network_client):
    public_ip_addess_params = {
        'location': LOCATION,
        'public_ip_allocation_method': 'Dynamic'
    }
    creation_result = network_client.public_ip_addresses.create_or_update(
        GROUP_NAME,
        'myIPAddress',
        public_ip_addess_params
    )

    return creation_result.result()

def create_vnet(network_client):
    vnet_params = {
        'location': LOCATION,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16']
        }
    }
    creation_result = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        'myVNet',
        vnet_params
    )
    return creation_result.result()

def create_subnet(network_client):
    subnet_params = {
        'address_prefix': '10.0.0.0/24'
    }
    creation_result = network_client.subnets.create_or_update(
        GROUP_NAME,
        'myVNet',
        'mySubnet',
        subnet_params
    )

    return creation_result.result()

def create_nic(network_client):
    subnet_info = network_client.subnets.get(
        GROUP_NAME,
        'myVNet',
        'mySubnet'
    )
    publicIPAddress = network_client.public_ip_addresses.get(
        GROUP_NAME,
        'mySubnet'
    )
    nic_params = {
        'location': LOCATION,
        'ip_configurations': [{
            'name': 'myIPConfig',
            'public_ip_address': publicIPAddress,
            'subnet': {
                'id': subnet_info.id
            }
        }]
    }
    creation_result = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        'myNic',
        nic_params
    )

    return creation_result.result()

def create_vm(network_client, compute_client):
    nic = network_client.network_interfaces.get(
        GROUP_NAME,
        'myNic'
    )
    avset = compute_client.availability_sets.get(
        GROUP_NAME,
        'myAVSet'
    )
    vm_parameters = {
        'location': LOCATION,
        'os_profile': {
            'computer_name': VM_NAME,
            'admin_username': 'yourusername',
            'admin_password': 'Yourpassword01!'
        },
        'hardware_profile': {
            'vm_size': 'Standard_DS1'
        },
        'storage_profile': {
            'image_reference': {
                'publisher': 'Canonical',
                'offer': 'UbuntuServer',
                'sku': '18.04-LTS',
                'version': 'latest'
            }
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic.id
            }]
        },
        'availability_set': {
            'id': avset.id
        }
    }
    creation_result = compute_client.virtual_machines.create_or_update(
        GROUP_NAME,
        VM_NAME,
        vm_parameters
    )

    return creation_result.result()

def start_vm(compute_client):
    compute_client.virtual_machines.start(GROUP_NAME, VM_NAME)

if __name__ == "__main__":

    credentials = get_credentials()

    resource_group_client = ResourceManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credentials,
        SUBSCRIPTION_ID
    )

create_resource_group(resource_group_client)
print("\nCreating Resource Group")

create_availability_set(compute_client)
print("\nCreating Availability Set")

creation_result = create_public_ip_address(network_client)
print("\nCreating Public IP")

creation_result = create_vnet(network_client)
print("\nCreating VNET")

creation_result = create_subnet(network_client)
print("\nCreating Subnet")

creation_result = create_nic(network_client)
print("\nCreating NIC")

creation_result = create_vm(network_client, compute_client)
print("\nCreating Virtual Machine")

start_vm(compute_client)
print("\nComplete! Starting Virtual Machine")
