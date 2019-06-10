import json
import os

import xlrd
import requests


session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'aparna.pal.1994@gmail.com', ''
url = 'https://z3nplatformdevap.zendesk.com/api/v2/users/create_many.json'

payloads = []
users_dict = {'users': []}

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

book = xlrd.open_workbook(os.path.join(__location__, 'users_list.xlsx'))
sheet = book.sheet_by_name('Sheet1')

for row in range(1, sheet.nrows):
    if sheet.row_values(row)[2]:
        users_dict['users'].append(
            {
                'name': sheet.row_values(row)[2],
                'email': sheet.row_values(row)[3],
                'organization_id':int(sheet.row_values(row)[12]),
                'role':sheet.row_values(row)[4],
                'tags':sheet.row_values(row)[11],
                #'shared':'',
                #'shared_agent':'',
                #'details':'',
               #'notes':sheet.row_values(row)[5],
               # 'restricted_agent':'',
                'user_fields': {
                    'employee_id': sheet.row_values(row)[9],
                    'promotion_code': sheet.row_values(row)[10],
                    'subscription':sheet.row_values(row)[8],
                    'acme_id': int(sheet.row_values(row)[1])
                }
            }
        )

    if len(users_dict['users']) == 100:
        payloads.append(json.dumps(users_dict))
        users_dict = {'users': []}

if users_dict['users']:
    payloads.append(json.dumps(users_dict))

for payload in payloads:
    print(payload)
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.status_code))
        exit()
    print('Successfully imported a batch of users')
