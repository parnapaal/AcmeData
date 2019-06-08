import json
import requests


# Set the request parameters
url = 'https://z3nplatformdevap.zendesk.com/api/v2/user_fields.json'
user = 'aparna.pal.1994@gmail.com'
pwd = ''
headers = {'content-type': 'application/json'}

#data = {
 #       {"user_field":
          #   {"type": "integer", "title": "Acme ID",
    #   "description": "T", "active": "true", "key": "acme_id"}}
 #   }


data = { "user_field":{
      "type": "integer",
      "title": "Acme ID",
      "description": 'The Acme ID allows Acme to reference the users when comparing to their customer data store.',
      "active": "true",
      "key": "acme_id"
    }}



payload = json.dumps(data)

# Do the HTTP post request
response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)

# Check for HTTP codes other than 201 (Created)
if response.status_code != 201:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()

# Report success
print('Successfully created the custom user field.')
