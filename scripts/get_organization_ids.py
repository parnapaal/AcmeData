import os
import requests
import json
import pandas as pd

# Set the request parameters
url = 'https://z3nplatformdevap.zendesk.com/api/v2/organizations.json'

user = 'aparna.pal.1994@gmail.com'
pwd = ''

names = []
ids = []

while url:

    # Do the HTTP get request
    response = requests.get(url, auth=(user, pwd))

# Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

# Decode the JSON response into a dictionary and use the data
    data = response.json()



    group_list = data['organizations']

    for group in group_list:
        names.append(group['name'])
        ids.append(group['id'])
    url = data['next_page']



dict = {'IDs':ids,'Names':names}

df = pd.DataFrame(dict)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

path = os.path.join(__location__, 'organization_ids.csv')

df.to_csv(path)



