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
            self.clean_data()
            self.add_aparna()
        except FileNotFoundError:
            print('Wrong file or file path!')
            self.df = ""

#clean our data of non-ascii characters. If our column is called 'name', take out the '- CE' it shouldn't be here
    def clean_data(self):
        self.df = self.df.replace('_', 'underscore', regex=True)
        #print(self.df)

        #self.df = self.df.fillna("")
        #remove non-ascii's
        #self.df = self.df.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True

        #names = list(self.df)
        #trythis = self.df['domain_names'].str.replace("['()]", "")
        #print(trythis)
        #print(names)
        #if 'name' in list(self.df):
         #   self.df = self.df['name'].str.replace(' - CE', '', regex=True)

        if 'domain_names' in self.df.columns:
            #there is definitely a better way to do this -- come back here if you think of it - write this into commit
            self.df['domain_names'] = self.df['domain_names'].str.replace("['[()]", "").values
            self.df['domain_names'] = self.df['domain_names'].str.replace("[]]", "").values

        if 'name' in self.df.columns:
            names = self.df['name']
            is_number = names.str.isnumeric()
            true_here = is_number[is_number].index
            for ind in true_here:
                val = self.df.iloc[ind, 1]
                val = str(val) + '_flagged_for_inspection'
                self.df.iloc[ind, 1] = val

            self.df['name'] = self.df['name'].str.replace('[^\w\s#@/:%.,_-]', '')

        if 'notes' in self.df.columns:
            self.df['notes'] = self.df['notes'].str.replace('[^\w\s#@/:%.,_-]', '')

    def add_aparna(self):
        if 'name' in self.df.columns:
            self.df['name'] = self.df['name'].astype(str) + ' - aparna'




#return our self.dataframe
    def get_dataframe(self):
       return self.df

#replace our dataframe with another
    def replace_dataframe(self, dataframe):
        self.df = dataframe

#if entries are the exact same, delete one
    def delete_identical_entries(self):
       pass

#if entries are the same through name, email, and organization, and group, merge them
    def merge_similar_entries(self):
        pass

#check to see if two entries are similar enough to merge
    def is_it_similar_enough(self):
        pass

    def df_to_xlsx(self, string):
        string = string + '.xlsx'
        return self.df.to_excel(string, index=False)


