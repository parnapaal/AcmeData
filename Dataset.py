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

#if entries are the exact same, delete one
    def delete_identical_entries(self):
       pass

#if entries are the same through name, email, and organization, and group, merge them
    def merge_similar_entries(self):
        pass

#check to see if two entries are similar enough to merge
    def is_it_similar_enough(self):
        pass




