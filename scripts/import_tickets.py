import json
import xlrd
import requests


session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = 'aparna.pal.1994@gmail.com', 'Ferrar1_'
url = 'https://z3nplatformdevap.zendesk.com/api/v2/imports/tickets/create_many.json'



payloads = []
tickets_dict = {'tickets': []}
book = xlrd.open_workbook('tickets_list.xlsx')
sheet = book.sheet_by_name('Sheet1')

for row in range(1, sheet.nrows):
    if sheet.row_values(row)[2]:
        tickets_dict['tickets'].append(
            {
                'external_id': int(sheet.row_values(row)[0]),
                # this won't work probably
                'created_at': sheet.row_values(row)[2],
                'updated_at': sheet.row_values(row)[8],
                'subject':sheet.row_values(row)[3],
                'description':sheet.row_values(row)[4],
                'status':sheet.row_values(row)[5],
                'requester_id':int(sheet.row_values(row)[7]),
                'submitter_id':int(sheet.row_values(row)[6]),
                'asignee_id':int(sheet.row_values(row)[1]),
                #'organization_id':'',
                #'group_id':'',
                'due_at':sheet.row_values(row)[9],
                'tags':sheet.row_values(row)[17],
                'custom_fields': [
                    {
                        #subscription
                        "id": 360020179373,
                        "value:": sheet.row_values(row)[16],
                    },
                    {
                        # emp id
                        "id": 360020179393,
                        "value": int(sheet.row_values(row)[13]),
                    },
                    {
                        #about
                        "id": 360020197314,
                        "value": sheet.row_values(row)[10],
                    },
                    {
                        # department
                        "id": 360020179413,
                        "value": sheet.row_values(row)[12],
                    },
                    {
                        # product info
                        "id": 360020197334,
                        "value": sheet.row_values(row)[14],
                    },
                    {
                        # business name
                        "id": 360020197354,
                        "value": sheet.row_values(row)[11],
                    },
                   # {
                    #    # start date
                     #   "id": 360020197374,
                      #  "value": sheet.row_values(row)[15]
                    #}

                ]
            }
        )


    if len(tickets_dict['tickets']) == 100:
        payloads.append(json.dumps(tickets_dict))
        tickets_dict = {'tickets': []}

if tickets_dict['tickets']:
    payloads.append(json.dumps(tickets_dict))

for payload in payloads:
    print(payload)
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.status_code))
        exit()
    print('Successfully imported a batch of users')
