import os
import requests
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.dns.models import ARecord, RecordSet
from azure.identity import DefaultAzureCredential

# Define the Azure credentials
credential = DefaultAzureCredential()

# Define Azure subscription id
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

# Define your DNS Zone and record name
dns_zone = os.getenv("DNS_ZONE")
record_name = os.getenv("DNS_RECORD")

# Create a DnsManagementClient instance
dns_client = DnsManagementClient(credential, subscription_id)

whoami = os.getenv("WHOAMI")
if not whoami:
    whoami = 'azure-dns-updater'

# Find public IP address
response = requests.get('https://api.ipify.org')
public_ip = response.text

try:
    record_set = dns_client.record_sets.get(
        resource_group_name=os.getenv("DNS_RESOURCE_GROUP"),
        zone_name=dns_zone,
        relative_record_set_name=record_name,
        record_type="A"
    )

    # Update the first record with the new IP (assuming it's the only one)
    record_set.a_records[0].ipv4_address = public_ip
except Exception as e:
    print("Record set doesn't exist, creating a new one")
    # If record doesn't exist, we create a new one
    record_set = RecordSet(ttl=600)
    record_set.a_records = [ARecord(ipv4_address=public_ip)]
    
record_set.metadata = {'updated_by': whoami}

# Update the record set in Azure DNS
dns_client.record_sets.create_or_update(
    resource_group_name=os.getenv("DNS_RESOURCE_GROUP"),
    zone_name=dns_zone,
    relative_record_set_name=record_name,
    record_type="A",
    parameters=record_set
)
