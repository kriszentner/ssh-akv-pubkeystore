# ssh-akv-pubkeystore
This is some simple code to make a centralized ssh public key store for a group of hosts.

# Setting it up
You'll need to get the following information to fill in your script:
## vault_name
When you make your Azure Key Vault, this is the name you give it.
## client_id
You'll get this when you make an app registration in AAD.
## secret
When you generate a client secret for your client ID, you'll get this.
## tenant
You can find this by using the Azure CLI command: az account show on the subscription
your Azure Key Vault is in.
```
az account show
{
  "environmentName": "AzureCloud",
  "id": "e1f5e208-9e4f-7d68-71d7-141dd843f2a7",
  "isDefault": true,
  "name": "My Subscription Name",
  "state": "Enabled",
  "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
  "tenantId": "30393678-1231-31c2-3cad-6788a4956788",
  "user": {
    "name": "me@contoso.com",
    "type": "user"
  }
}
```
You can find more info [here](https://blogs.msdn.microsoft.com/kaevans/2016/10/31/using-azure-keyvault-to-store-secrets/)
