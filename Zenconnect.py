import math

import pandas as pd
import numpy as np
import requests
import json


#This class handles our datasets. It is responsible for the data manipulation and conversion responsible for taking a
#csv, turning it into a dataframe, and then turning those pandas dataframe entries into strings suitable for json
# interpretation
class Zenconnect(object):

    def __init__(self):
        # Set the request parameters
        self.url = 'https://z3nplatformdevap.zendesk.com/api/v2/'
        self.user = 'aparna.pal.1994@gmail.com'
        self.pwd = 'Ferrar1_'


    def get(self, address):
        self.url = self.url + address + '.json'


    def create(self):
        pass

    def create_many(self):
        pass

    def base_connection(self, get_put_):
        # Do the HTTP get request
        response = requests.get(self.url, auth=(self.user, self.pwd))

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()

        #print(json.dumps(data, indent=2))
        #print(json.dumps(parsed, indent=4, sort_keys=True))

        # Example 1: Print the name of the first group in the list
        # print( 'First group = ', data['groups'][0]['name'] )

        # Example 2: Print the names of each organization
        group_list = data['users']
        for group in group_list:
            print(group['name'])