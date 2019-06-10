import json
import os
import pandas as pd

import xlrd
import requests


session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'aparna.pal.1994@gmail.com', ''
url = 'https://z3nplatformdevap.zendesk.com/api/v2/organizations.json'
user = 'aparna.pal.1994@gmail.com'
pwd = ''
headers = {'content-type': 'application/json'}

payloads = []
organization_dict = {'organization': []}




__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
book = xlrd.open_workbook(os.path.join(__location__, 'org_list.xlsx'))
sheet = book.sheet_by_name('Sheet1')
path = os.path.join(__location__, 'org_list.xlsx')

count = 0

for row in range(1, sheet.nrows):
    if sheet.row_values(row)[1]:
        domain = sheet.row_values(row)[2].replace("[", "").replace("]","").replace("'","").replace("(","").replace(")","")
        domain = domain.split(",")
        val = {
                'name': sheet.row_values(row)[1],
                # this won't work probably
                'domain_names': domain,
                'details': sheet.row_values(row)[3],
                'notes': sheet.row_values(row)[4],
                # this also might not work
                'tags': sheet.row_values(row)[6],
                'organization_fields': {'region': sheet.row_values(row)[5]
                                        }
            }
        data = {"organization": val }
        payload = json.dumps(data)
        response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)

        if response.status_code != 201:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            print(val)
            exit()

        count = count + 1

        # Report success
        print('Successfully created the organization.')

path = os.path.join(__location__, 'org_list.xlsx')

df = pd.read_excel(os.path.join(__location__, 'org_list.xlsx'))
df = df.iloc[count:]
df.to_excel(path, index=False)
print(df)

if len(df.index) > 0:
    os.system('python scripts/import_orgs.py')
print('finished')





