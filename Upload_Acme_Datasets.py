import os
import pandas as pd


from AcmeData.Dataset import Dataset
import AcmeData.scripts
import json
import xlrd
import requests

def join_tables():
    pass

def set_path(string):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    path = os.path.join(__location__, string)

    return path

def combine_users_and_org_names(organizations, users):

    organization_names = organizations.iloc[:, 0:2]
    organization_names = organization_names.set_index('id')
    organization_names = organization_names.rename(index=str, columns={"name": "org_name"})
    user = users.rename(index=str, columns={"name": "user_name"})
    s = users['organization_id'].str.split(',').apply(pd.Series, 1).stack()
    s.index = s.index.droplevel(-1)
    s.name = 'organization_id'
    del users['organization_id']
    users = users.join(s)
    # take out extra formatting from the organization id like [ and  ''
    users['organization_id'] = users['organization_id'].map(lambda x: x.lstrip("[' ").rstrip("'] "))
    # set our index for the join
    users = users.set_index('organization_id')
    # this is our table of users with their organization names
    result = pd.concat([users, organization_names], axis=1, join_axes=[users.index])
    return result

def update_user_org_ids(org_ids, orgs_and_names):

    org_ids['Names'] = org_ids['Names'].str.replace(' - aparna', '', regex=True)
    org_ids['Names'] = org_ids['Names'].str.replace('_flagged_for_inspection', '', regex=True)
    org_ids['Names'] = org_ids['Names'].str.replace('underscore', '_', regex=True)

    orgs_and_names['org_name'] = orgs_and_names['org_name'].str.replace(' - aparna', '', regex=True)
    orgs_and_names['org_name'] = orgs_and_names['org_name'].str.replace('_flagged_for_inspection', '', regex=True)
    orgs_and_names['org_name'] = orgs_and_names['org_name'].str.replace('underscore', '_', regex=True)

    #orgs_and_names = orgs_and_names.drop('organization_id', axis=1)
    orgs_and_names = orgs_and_names.set_index('org_name')

    org_ids = org_ids.set_index('Names')


    org_ids = org_ids.loc[:, ~org_ids.columns.str.contains('^Unnamed')]

    result = pd.concat([orgs_and_names, org_ids], axis=1, join_axes=[orgs_and_names.index])

    return result


if __name__ == '__main__':
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    orgs = Dataset('csv_data/organizations.csv')
    orgs.df_to_xlsx('scripts/org_list')

    path = os.path.join(__location__, 'csv_data/users.csv')
    users = Dataset(path)

    orgs_and_names = combine_users_and_org_names(orgs.df, users.df)

    path = set_path('scripts/get_organization_ids.py')
    os.system('python ' + path)

    path = set_path('scripts/organization_ids.csv')
    org_ids = pd.read_csv(path)

    combined = update_user_org_ids(org_ids, orgs_and_names)
    users.replace_dataframe(combined)
    users.df.to_excel('checking.xlsx')




    #os.system('python scripts/import_orgs.py')

#    path = set_path('scripts/add_custom_user_field.py')
#   os.system('python ' + path)


