import pandas as pd

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
        pass

    def to_json(self):
        pass

    def upload(self):
        pass