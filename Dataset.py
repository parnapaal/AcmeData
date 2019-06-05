import math

import pandas as pd
import numpy as np


#This class handles our datasets. It is responsible for the data manipulation and conversion responsible for taking a
#csv, turning it into a dataframe, and then turning those pandas dataframe entries into strings suitable for json
# interpretation
class Dataset(object):

    dict = ['']
    #initialize our class with our file name and our dataframe
    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.df = pd.read_csv(fileName)
        except FileNotFoundError:
            print('Wrong file or file path!')
            self.df = ""

        #self.clean_data()

#clean our data of non-ascii characters. If our column is called 'name', take out the '- CE' it shouldn't be here
    def clean_data(self):
        self.df = self.df.fillna("")
        self.df = self.df.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True)

        if 'name' in self.df.columns:
            self.df = self.df['name'].str.replace(' - CE', '', regex=True)


#return our self.dataframe
    def get_dataframe(self):
       return self.df

#replace our dataframe with another
    def replace_dataframe(self, dataframe):
        self.df = dataframe


#chunkify our dataframe into pieces small enough for the zendesk API to handle
    def create_hundred_entity_chunks(self):
        num_full_dfs = math.floor(len(self.df)/100)
        dfs = []
        for i in range(num_full_dfs):
            dfs.append(pd.DataFrame(self.df.iloc[:(i+1)*100,:]))

        dfs.append(pd.DataFrame(self.df.iloc[(i+1)*100:]))
        return dfs

#if entries are the exact same, delete one
    def delete_identical_entries(self):
       pass

#if entries are the same through name, email, and organization, and group, merge them
    def merge_similar_entries(self):
        pass

#check to see if two entries are similar enough to merge
    def is_it_similar_enough(self):
        pass
#take a pandas row and convert it into a string that we can pass to our ZendeskConnector class to upload to our database
    def to_json_format(self, df_entry, dataset):
        if dataset == 'organization':
            data = {"name":df_entry[0], "domain_names":df_entry[1], "details":df_entry[2], "notes":df_entry[3], "tags":df_entry[5], "organization_fields":{"region": df_entry[4]}}
            if self.custom_field_is_null(df_entry[4]):
                del data["organization_fields"]
            return data

        if dataset == 'users':
            data= {
                "name": df_entry[0],
                "email":df_entry[1],
                "organization_id": df_entry[2],
                "role": df_entry[3],
                "tags": df_entry[4],
                "active": df_entry[5],
                "shared": df_entry[6],
                "shared_agent": df_entry[7],
                "notes": df_entry[8],
                "default_group_id": df_entry[9],
                "user_fields": {
                    "employee_id": df_entry[10],
                    "promotion_code": df_entry[11],
                    "subscription": df_entry[12]
                }}
            return data
        return ""

#return a boolean basod on if our custom field is null
    def custom_field_is_null(self,string):
        if string == "":
            return True

        return False

#create a ZendeskConnector instance for an upload event -- this will use the create_many feature of the Zendesk API
    def upload(self):
        pass