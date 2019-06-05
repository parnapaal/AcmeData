import math

import pandas as pd
import numpy as np

class Dataset(object):

    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.df = pd.read_csv(fileName)
        except FileNotFoundError:
            print('Wrong file or file path!')
            self.df = ""

        self.clean_data()


    def clean_data(self):
        pass


    def get_dataframe(self):
       return self.df

    def replace_dataframe(self, dataframe):
        self.df = dataframe

    def create_hundred_entity_chunks(self):
        num_full_dfs = math.floor(len(self.df)/100)
        dfs = []
        print(len(self.df))
        for i in range(num_full_dfs):
            dfs.append(pd.DataFrame(self.df.iloc[:(i+1)*100,:]))
            self.df = self.df.iloc[(i+1)*100,:]
            print(len(self.df))

        return dfs
    def to_json(self):
        pass

    def upload(self):
        pass