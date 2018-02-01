#!/usr/bin/env python
import json
import pprint
import sys
import re
from azure.keyvault import KeyVaultClient
from azure.common.credentials import ServicePrincipalCredentials

vault_name = ''
client_id = ''
secret = ''
tenant = ''
# We need at least one arg for the username
if len(sys.argv) < 2:
  print "usage: ./set_ssh_key.py alias authorized_keys_file"
  sys.exit()

# Get our username, and lowercase it
username = sys.argv[1].lower()
authorized_keys_file = sys.argv[2]

# Check if this all letters
if not re.search('[a-z]',username):
  print "not a valid username"
  sys.exit()
if re.search('\.',username):
  alias = username.split('.')[1]
else:
  alias = username

# Our AKV creds
KEY_VAULT_URI="https://{0}.vault.azure.net/".format(vault_name)
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=secret,
    tenant=tenant
)

client = KeyVaultClient(
    credentials
)
with open(authorized_keys_file, 'r') as myfile:
  keys = myfile.read()
try:
  secret = client.set_secret(KEY_VAULT_URI,alias,keys)
except:
  print "Secret Update Failed"
  sys.exit(1)

try:
  secret.value
except NameError:
  print "No value returned from KeyVault"
  sys.exit(1)
else:
  print "New Secret Value for {0}".format(username)
  print secret.value
