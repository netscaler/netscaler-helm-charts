#! /usr/bin/python3
#
# Script to generate authorization bearer token
#

import argparse
import requests
import json

# The US-based service api-us.cloud.com will work for deployments in any geo. 
# However, should you wish to use a local service, matching a customer 
# geography, use api-eu.cloud.com for EU, or api-ap-s.cloud.com for Asia 
# Pacific South.
TOKEN_URL = 'https://api-us.cloud.com/cctrustoauth2/root/tokens/clients'

# Parse id's from the command line
# Note use of the UUID type - invalid UUID's will be automatically rejected
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--accessID", required=True, help="Access Client ID")
parser.add_argument("-s", "--accessSecret", required=True, help="Access Client secret")
args = parser.parse_args()

# Obtain bearer token from authorization server
response = requests.post(TOKEN_URL, data={
  'grant_type': 'client_credentials',
  'client_id': {args.accessID},
  'client_secret': {args.accessSecret}
})
dictionary = json.loads(response.text)
token = dictionary['access_token']
print(token)