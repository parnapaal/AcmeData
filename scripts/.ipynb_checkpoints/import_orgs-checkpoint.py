import json
import xlrd
import requests


session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'aparna.pal.1994@gmail.com', 'Ferrar1_'
url = 'https://z3nplatformdevap.zendesk.com/api/v2/organizations/create_many.json'

payloads = []

org_dict = {'organizations': []}
book = xlrd.open_workbook('org_list.xlsx')
sheet = book.sheet_by_name('Sheet1')

for row in range(1, sheet.nrows):
    print(row)
    if sheet.row_values(row)[2]:
        print('got here')
        org_dict['organizations'].append(
            {
                'name': sheet.row_values(row)[1],
                #this won't work probably
                'domain_names' : sheet.row_values(row)[2],
                'details': sheet.row_values(row)[3],
                'notes': sheet.row_values(row)[4],
                #this also might not work
                'tags' : sheet.row_values(row)[6],
                'organization_fields': {'region': sheet.row_values(row)[5]}
            }
        )

    if len(org_dict['organizations']) == 100:
        payloads.append(json.dumps(org_dict))
        org_dict = {'organizations': []}

if org_dict['organizations']:
    payloads.append(json.dumps(org_dict))

for payload in payloads:
    print(payload)
    print(org_dict)
    #response = session.post(url, data=payload)
    #if response.status_code != 200:
        #print('Import failed with status {}'.format(response.status_code))
        #exit()
    #print('Successfully imported a batch of orgs')