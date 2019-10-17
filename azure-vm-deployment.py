from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import DiskCreateOption

SUBSCRIPTION_ID = 'fd8a5d07-d857-49d6-aecc-f5ea0471de9b'
GROUP_NAME = 'TCG-GROUP-PROD'
LOCATION = 'eastus'
VM_NAME = 'TCG-VM-01'

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id = 'ad25cf01-1c48-4cf5-aba5-543dfa75dd30',
        secret = 'kdT1mMwhl1DWuKM.W/MIzJmqN-.VcI38',
        tenant = '22b17e1f-a206-43ec-897d-511184d5b503'
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
        'myIPAddress'
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
            'admin_username': 'adminuser',
            'admin_password': 'adminuser01!'
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
#input('Resource group created. Press enter to continue...')

create_availability_set(compute_client)
print("\nCreating Availability Set")
#input('Availability set created. Press enter to continue...')

creation_result = create_public_ip_address(network_client)
print("\nCreating Public IP")
#print(creation_result)
#input('Press enter to continue...')

creation_result = create_vnet(network_client)
print("\nCreating VNET")
#print(creation_result)
#input('Press enter to continue...')

creation_result = create_subnet(network_client)
print("\nCreating Subnet")
#print(creation_result)
#input('Press enter to continue...')

creation_result = create_nic(network_client)
print("\nCreating NIC")
#print(creation_result)
#input('Press enter to continue...')

creation_result = create_vm(network_client, compute_client)
print("\nCreating Virtual Machine")
#print(creation_result)
#input('Press enter to continue...')

start_vm(compute_client)
print("\nComplete. Starting Virtual Machine")
#input('Press enter to continue...')