import os

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









if __name__ == '__main__':
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    orgs = Dataset('csv_data/organizations.csv')
    orgs.df_to_xlsx('scripts/org_list')

    path = os.path.join(__location__, 'csv_data/users.csv')
    users = Dataset(path)




    #os.system('python scripts/import_orgs.py')

#    path = set_path('scripts/add_custom_user_field.py')
#   os.system('python ' + path)


