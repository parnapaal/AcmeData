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

        #replace na's with '' to avoid NaN errors
        self.df = self.df.fillna('')

        #cleaning for domain names -- take out extra parentheses -- if I have time, I would like to change this
        #tot use some numpy extraction commands
        if 'domain_names' in self.df.columns:
            #there is definitely a better way to do this -- come back here if you think of it - write this into commit
            self.df['domain_names'] = self.df['domain_names'].str.replace("['[()]", "").values
            self.df['domain_names'] = self.df['domain_names'].str.replace("[]]", "").values
            self.df['domain_names'] = self.df['domain_names'].replace('_', 'underscore', regex=True)

        #if a name is just a number, there is a chance something went wrong -- this needs to be flagged -- see above
        #note about numpy extraction as well
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


    #add my name to the tags list -- there are a few commands for tags cleanus below that need to be migrated
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
    #def delete_identical_entries(self):
        #self.df = self.df.drop_duplicates(subset=['name','email'])


    #the next 4 methods deal with merging on identical emails
    def dealing_with_identical_emails(self):
        #send to other methods to merge together entries on emails
        df = self.merge_similar_entries()
        df = self.pick_a_merged_subscription(df)
        df = self.pick_a_merged_role(df)

        #check for a flag in tags that tells us that the multiple entry is definitely the same person
        not_flagged = df.loc[df['tags'] != 'email_flagged']['email']
        # print(df.loc[df['tags'] == 'email_flagged'])

        #drop the duplicates within self.df, but save the information we need for our 'new' row
        for email in not_flagged:
            rows_we_need_to_update = self.result.loc[self.result['email'] == email]
            ids_to_delete = rows_we_need_to_update['id'].to_list()
            tags_to_add = ''
            notes_to_add = ''

            # delete the rows with shared info
            for ids in ids_to_delete:
                tags_to_add = rows_we_need_to_update.loc[rows_we_need_to_update['id'] == ids][
                                  'tags'].values + ", " + tags_to_add
                notes_to_add = rows_we_need_to_update.loc[rows_we_need_to_update['id'] == ids][
                                   'notes'].values + ", " + notes_to_add

                self.df = self.df[self.df['id'] != ids]

            emp_id = rows_we_need_to_update.loc[rows_we_need_to_update['id'] == ids]['employee_id'].values

            #here are all of our merged and simplified values -- they should be added back into our dataframe
            look_here = df.loc[df['email'] == email]

            all_ids = ids_to_delete
            #this command extracts strings from the arrays
            all_ids = ' '.join(map(str, all_ids))

            #here are all the merged features we are adding
            name = look_here['name'].values
            email = look_here['email'].values
            org_id = look_here['organization_id'].values
            role = look_here['role'].values
            active = look_here['active'].values
            api_subscription = look_here['api_subscription'].values
            promotion_code = look_here['promotion_code'].values

            toadd = {'id': ids_to_delete[0], 'name': ' '.join(map(str, name)), 'email': ' '.join(map(str, email)),
                     'organization_id': ' '.join(map(str, org_id)), 'role':' '.join(map(str, role)),
                     'active':' '.join(map(str, active)),
                     'notes': notes_to_add,
                     'api_subscription': ' '.join(map(str, api_subscription)), 'employee_id': emp_id,
                     'promotion_code': ' '.join(map(str, promotion_code)), 'tags': tags_to_add + look_here['tags'].values +
                                                                                   ', ' + all_ids}

            #append 'toadd' to our dataframe
            self.df = self.df.append(toadd, ignore_index=True)
            return self.df

#if entries are the same through name, email, and organization, and group, merge them
    def merge_similar_entries(self):
        #groups entries based on whether or not identical strings within 'email' are found
        self.result = pd.concat(g for _, g in self.df.groupby("email") if len(g) > 1)
        result_emails = list(set(self.df['email']))

        similar_entries = []
        for email in result_emails:
            #handle merges by email
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

        #iterate through our dataframe of repeated values -- if they all have the same name -- they can be condensed down
        for i, row in df.iterrows():
            names = row['name'].split(',')
            same_names = all(elem.strip() == names[0] for elem in names)

            if same_names:
                df.loc[df['name'] == row['name'], 'name'] = names[0]

            #if they do not have the same name, add a flag in tags to ensure someone looks at these values again
            else:
                similar_entries.append(df)
                df.loc[df['name'] == row['name'], 'tags'] = 'email_flagged'
        df = df.fillna('email_flagged')
        df['email'].replace('', np.nan, inplace=True)
        df.dropna(subset=['email'], inplace=True)
        return df


    #pick the highest subscription seen within a merged set
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

    #pick the highest role seen within a merged set
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

    #export to excel -- for our scripts
    def df_to_xlsx(self, string):
        string = string + '.xlsx'
        #return self.df.to_excel(string, index=False)


