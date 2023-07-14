Azure DNS Updater
=================
[![License](https://img.shields.io/github/license/qwerty-iot/azure-dns-updater)](https://opensource.org/licenses/MPL-2.0)
This is a simple project to facilitate updating dynamic DNS settings in Azure's DNS zones.  The most common use case is to update remote sites that may be behind a dynamic address.

Creating a service principal in Azure
-------------------------------------
To use this container, you will need a service principal with access to your DNS zone.  Here is a procedure to create it with the Azure CLI:
```
az ad sp create-for-rbac --name ServicePrincipalName --role "DNS Zone Contributor" --scopes /subscriptions/{SubID}/resourceGroups/{ResourceGroupName}/providers/Microsoft.Network/dnszones/{your_dns_zone} --years 20
```

Running via Docker
------------------
```
docker run -e AZURE_SUBSCRIPTION_ID=<your-subscription-id> \
           -e AZURE_TENANT_ID=<your-tenant-id> \
           -e AZURE_CLIENT_ID=<your-client-id> \
           -e AZURE_CLIENT_SECRET=<your-client-secret> \
		   -e DNS_ZONE=<your-zone> \
		   -e DNS_RESOURCE_GROUP=<your-group> \
		   -e DNS_RECORD=<your-record> \
           ghcr.io/qwerty-iot/azure-dns-updater/azure-dns-updater:latest
```

Running via Kubernetes
----------------------
This will create the required secret, and a cron job that runs every hour.
```
kubectl create secret generic azure-creds \
  --from-literal=subscription_id=<your-subscription-id> \
  --from-literal=tenant_id=<your-tenant-id> \
  --from-literal=client_id=<your-client-id> \
  --from-literal=client_secret=<your-client-secret> \
  --from-literal=dns_resource_group=<your-dns-resource-group> \
  --from-literal=dns_zone=<your-dns-zone> \
  --from-literal=dns_record=<your-dns-record>
  
kubectl apply -f azure-dns-updater.yaml
```

License
-------

Mozilla Public License Version 2.0