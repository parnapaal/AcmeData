import os

from AcmeData.Dataset import Dataset
import AcmeData.scripts
import json
import xlrd
import requests











if __name__ == '__main__':
    orgs = Dataset('csv_data/organizations.csv')
    orgs.df_to_xlsx('scripts/org_list')

    #os.system('python scripts/import_orgs.py')
