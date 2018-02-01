# ssh-akv-pubkeystore
These are a couple scripts you can use to make Azure Key Vault a central store for ssh public keys, instead of managing many local ~/.ssh/authorized_keys files. This also has the benefit that a user's home dir doesn't need to exist for this to work.

You'll need to make your own Azure Key Vault, as well as a client with access to it, and the client's secret (see below).

I've used this in the past with some centralized user management systems such as Winbind (which is why the username supports DOMAIN.user as a lookup method), and database based management systems.

This simply makes the username the key, and the contents of authorized_keys the value in AKV. Once you set up your AKV and script variables, testing is as simple as:

```
./set_ssh_key.py username authorized_keys_file
```
```
./get_ssh_key.py username
```

# Getting the Script Variables
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
  "tenantId": "30393678-1231-31c2-3cad-6788a4956788",
  "user": {
    "name": "me@contoso.com",
    "type": "user"
  }
}
```
You can find more info [here](https://blogs.msdn.microsoft.com/kaevans/2016/10/31/using-azure-keyvault-to-store-secrets/)

# Setting up the ssh server
Once you have the script variables, you can drop the script into /etc/ssh.
Create a cmd user like sshauthcmd user, then and edit your /etc/ssh/sshd_config like so:
```
AuthorizedKeysCommandUser sshauthcmduser
AuthorizedKeysCommand /etc/ssh/get_ssh_key.py
```
# Getting keys into Azure Key Vault
You could adapt ./set_ssh_key.py as a wrapper to a web frontend, or you could do something similar to what I do, which is have a host people can ssh into with a password, and have the users populate their authorized_keys_file. After which, a cron job puts that file into AKV for them via a script in crontab:
```
#!/bin/bash
marker="/root/akvsyncmarker"
if ! [ -f $marker ];then
  for i in `find /home/*/.ssh/authorized_keys`;do
    touch $marker
    useralias=`echo $i|awk -F/ '{ print $3 }'`
    /root/set_ssh_key.py $useralias $i
  done
else
  for i in `find /home/*/.ssh/authorized_keys -newer $marker`;do
    touch $marker
    useralias=`echo $i|awk -F/ '{ print $3 }'`
    /root/set_ssh_key.py $useralias $i
  done
fi
# Remove private keys from the server.
find /home -name id_rsa -exec rm {} \;
find /home -name id_dsa -exec rm {} \;
```
