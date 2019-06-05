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

    def to_json(self, identifier):
        if identifier == 'organization':
            print('got here!')
        pass

    def upload(self):
        pass