import json
import xlrd
import requests


session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'aparna.pal.1994@gmail.com', 'Ferrar1_'
url = 'https://z3nplatformdevap.zendesk.com/api/v2/users/create_many.json'

payloads = []
users_dict = {'users': []}
book = xlrd.open_workbook('users_list.xlsx')
sheet = book.sheet_by_name('Sheet1')

for row in range(1, sheet.nrows):
    if sheet.row_values(row)[2]:
        users_dict['users'].append(
            {
                'name': sheet.row_values(row)[2],
                'email': sheet.row_values(row)[3],
                'user_fields': {'member_level': sheet.row_values(row)[7]}
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