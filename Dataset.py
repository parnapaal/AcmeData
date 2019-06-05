import math

import pandas as pd
import numpy as np

class Dataset(object):

    dict = ['']

    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.df = pd.read_csv(fileName)
        except FileNotFoundError:
            print('Wrong file or file path!')
            self.df = ""

        #self.clean_data()


    def clean_data(self):
        self.df = self.df.fillna("")
        self.df = self.df.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True)

        if 'name' in self.df.columns:
            self.df = self.df['name'].str.replace(' - CE', '', regex=True)



    def get_dataframe(self):
       return self.df

    def replace_dataframe(self, dataframe):
        self.df = dataframe

    def create_hundred_entity_chunks(self):
        num_full_dfs = math.floor(len(self.df)/100)
        dfs = []
        for i in range(num_full_dfs):
            dfs.append(pd.DataFrame(self.df.iloc[:(i+1)*100,:]))

        dfs.append(pd.DataFrame(self.df.iloc[(i+1)*100:]))
        return dfs

    def delete_identical_entries(self):
       pass

    def merge_similar_entries(self):
        pass

    def is_it_similar_enough(self):
        pass

    def to_json_format(self, df_entry, dataset):
        if dataset == 'organization':
            data = {"name":df_entry[0], "domain_names":df_entry[1], "details":df_entry[2], "notes":df_entry[3], "tags":df_entry[5], "organization_fields":{"region": df_entry[4]}}
            if self.custom_field_is_null(df_entry[4]):
                del data["organization_fields"]

            return data
        return ""

    def custom_field_is_null(self,string):
        if string == "":
            return True

        return False


    def upload(self):
        pass