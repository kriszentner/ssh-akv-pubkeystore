#!/usr/bin/env python
import json
import pprint
import sys
import re
from azure.keyvault import KeyVaultClient
from azure.common.credentials import ServicePrincipalCredentials

vault_name = 'mykeyvault'
client_id = 'my_client_id'
secret = 'my_secret'
tenant = 'my_tenant'

# We need at least one arg for the username
if len(sys.argv) == 1:
  print "not a valid username"
  sys.exit()

# Get our username, and lowercase it
username = sys.argv[1].lower()

# Check if this all letters
if not re.search('[a-z]',username):
  print "not a valid username"
  sys.exit()
if re.search('\.',username):
  alias = username.split('.')[1]
else:
  alias = username

KEY_VAULT_URI="https://{0}.vault.azure.net/".format(vault_name)
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=secret,
    tenant=tenant
)

client = KeyVaultClient(
    credentials
)
try:
  secret = client.get_secret(KEY_VAULT_URI,alias,'')
except:
  pass

try:
  secret.value
except NameError:
  print "No value returned from KeyVault"
  sys.exit(1)
else:
  print secret.value
