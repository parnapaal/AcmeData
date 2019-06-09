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

        self.df = self.df.fillna('')

        if 'domain_names' in self.df.columns:
            #there is definitely a better way to do this -- come back here if you think of it - write this into commit
            self.df['domain_names'] = self.df['domain_names'].str.replace("['[()]", "").values
            self.df['domain_names'] = self.df['domain_names'].str.replace("[]]", "").values
            self.df['domain_names'] = self.df['domain_names'].replace('_', 'underscore', regex=True)

        if 'name' in self.df.columns:
            names = self.df['name']
            is_number = names.str.isnumeric()
            true_here = is_number[is_number].index
            for ind in true_here:
                val = self.df.iloc[ind, 1]
                val = str(val) + '_flagged_for_inspection'
                self.df.iloc[ind, 1] = val

            self.df['name'] = self.df['name'].str.replace('[^\w\s#@/:%.,_-]', '')
            #self.df['name'] = self.df['name'].replace('_', 'underscore', regex=True)


    def add_aparna(self):
        tags = self.df['tags']
        newtags = []
        for tag in tags:
            try:
                if tag == '[]':
                    tag = "'aparna'"

                else:
                    tag = tag.replace(']', ", 'aparna'")

            except:
                print('something is wrong')

            tag = tag.replace('underscore', '_')
            tag = tag.replace("'", '')
            tag = tag.replace('[', '')

            newtags.append(tag)

        self.df = self.df.drop("tags", axis=1)
        self.df['tags'] = newtags

    #return our self.dataframe
    def get_dataframe(self):
       return self.df

#replace our dataframe with another
    def replace_dataframe(self, dataframe):
        self.df = dataframe

#if entries are the exact same, delete one
    def delete_identical_entries(self):
        self.df = self.df.drop_duplicates(subset=['name','email'])

    def dealing_with_identical_emails(self):
        df = self.users.merge_similar_entries()
        df = self.users.pick_a_merged_role(df)
        pass

#if entries are the same through name, email, and organization, and group, merge them
    def merge_similar_entries(self):
        self.result = pd.concat(g for _, g in self.df.groupby("email") if len(g) > 1)
        result_emails = list(set(self.df['email']))
        similar_entries = []
        for email in result_emails:
            result_for_this_email = self.result.loc[self.result['email'] == email]
            df = self.result.groupby('email').agg({'email': 'first',
                                              'name': ', '.join,
                                              'role': ', '.join,
                                              'active': 'first',
                                              'api_subscription': ', '.join,
                                              'promotion_code': ', '.join,
                                              'role': ', '.join,
                                              'organization_id': ', '.join,
                                              'tags': 'first'
                                              }).reset_index(drop=True)

        for i, row in df.iterrows():
            names = row['name'].split(',')
            same_names = all(elem.strip() == names[0] for elem in names)

            if same_names:
                df.loc[df['name'] == row['name'], 'name'] = names[0]

            else:
                similar_entries.append(df)
                df.loc[df['name'] == row['name'], 'tags'] = 'email_flagged'
        df = df.fillna('email_flagged')
        df['email'].replace('', np.nan, inplace=True)
        df.dropna(subset=['email'], inplace=True)
        return df

    def pick_a_merged_subscription(self, df):
        for i, row in df.iterrows():
           if row['tags'] != 'flagged':
               subscription = row['api_subscription']
               if 'gold' in subscription:
                   df.loc[df['name'] == row['name'], 'api_subscription'] = 'plan_gold'

               elif 'silver' in subscription:
                   df.loc[df['name'] == row['name'], 'api_subscription'] = 'plan_silver'

               else:
                   df.loc[df['name'] == row['name'], 'api_subscription'] = 'plan_bronze'
        return df
    def pick_a_merged_role(self,df):
        for i, row in df.iterrows():
           if row['tags'] != 'flagged':
               roles = row['role']
               if 'admin' in roles:
                   df.loc[df['name'] == row['name'], 'role'] = 'admin'

               elif 'agent' in roles:
                   df.loc[df['name'] == row['name'], 'role'] = 'agent'

               else:
                   df.loc[df['name'] == row['name'], 'role'] = 'end_user'
        return df
#check to see if two entries are similar enough to merge
    def is_it_similar_enough(self):
        pass

    def df_to_xlsx(self, string):
        string = string + '.xlsx'
        return self.df.to_excel(string, index=False)


