import math
import unittest

import pandas as pd

from AcmeData.Dataset import Dataset


# Tests for our Dataset class
class TestDataset(unittest.TestCase):

    # set up instances for our testing
    def setUp(self):
        self.orgs = Dataset('csv_data/organizations.csv')
        self.users = Dataset('csv_data/users.csv')
        self.tickets = Dataset('csv_data/tickets.csv')

    # tear down our instances when a test is complete
    def tearDown(self):
        self.orgs = None
        self.users = None
        self.tickets = None

    # test that our files are opening correctly and are stored where we think they are
    def test_open_file_base_case(self):
        # confirm the datasets are being loaded in correctly through pandas by checking the size

        df = pd.read_csv('csv_data/organizations.csv')

        self.assertEqual(self.orgs.df.size, df.size)

    # if the file isn't found, let us know
    def test_if_file_not_found_throw_exception(self):
        organization = 'csv_data/organization.csv'
        set = Dataset(organization)

        self.assertTrue(set.df == "")

    # base case for cleaning our dataframe entries of ascii characters, NaNs and extra wordage in the name column --
    #clean data happens on instantiation so we do not need to call clean_data for the test methods of this class -- we
    #are just asserting that they happened correctly
    def test_clean_data_base_case(self):
        pass


    def test_clean_org_data(self):
        domain_col_at_zero = self.orgs.df['domain_names'].tolist()[0]

        self.assertEqual('1000bulbs.com, protonmail.com', domain_col_at_zero)

    def test_clean_data_when_name_is_number(self):
        pass

    def test_if_name_is_just_a_number_flag_it(self):

        self.assertEqual('123456789_flagged_for_inspection', self.orgs.df.iloc[4,1])

    def remove_non_ascii_symbols_during_cleaning(self):
        pass

    def test_find_similar_emails(self):
        result = pd.concat(g for _, g in self.users.df.groupby("email") if len(g) > 1)
        pass

    def test_merging_similar_entries(self):
        result = pd.concat(g for _, g in self.users.df.groupby("email") if len(g) > 1)
        #print(result['name'] + result['email'])
        find_this = result['email'].iloc[0]

        similar_entries = self.users.df.loc[self.users.df['email'] == find_this ]
        #print(similar_entries)
        #print(self.orgs.df)

            #if result[result['email'] == find_this_val]:
                #print('gotit')
            #print(match)
    # replace our dataframe within our instance with a new dataframe

    #flag_aparna() is called on instantiation - we are just checking that the tag is in place
    def test_flagged_as_aparna(self):
        self.assertEqual(self.users.df['tags'][0], 'aparna')

    def test_tags_are_stored_as_arrays(self):
        testing = self.orgs.df['tags'][10]

    def that_if_the_first_tag_value_is_null_it_is_removed(self):
        list_of_tags = self.orgs.df['tags']
        count = 0
        for tag in list_of_tags:
            if tag[0] == '':
                tags = tag.pop(0)
                count = count + 1
            #print(index)
        pass

    def test_merging_visitors(self):
        result = pd.concat(g for _, g in self.users.df.groupby("email") if len(g) > 1)


    def test_is_it_similar_enough(self):
        result = pd.concat(g for _, g in self.users.df.groupby("email") if len(g) > 1)
        result_emails = list(set(self.users.df['email']))
        similar_entries = []
        for email in result_emails:
            result_for_this_email = result.loc[result['email'] == email]
            df = result.groupby('email').agg({'email': 'first',
                                          'name': ', '.join,
                                          'role': ', '.join,
                                          'active': 'first',
                                          'api_subscription': ', '.join,
                                          'promotion_code': ', '.join,
                                          'role': ', '.join,
                                          'organization_id': ', '.join
                                              }).reset_index(drop=True)

        for i, row in df.iterrows():
            names = row['name'].split(',')
            same_names = all(elem.strip() == names[0] for elem in names)

            if same_names:
                df.loc[df['name'] == row['name'], 'name'] = names[0]

            similar_entries.append(df)

        def test_picking_merge_features():
            #pick a role

            #pick a subscription
            pass


    def test_replace_dataframe(self):
        set = Dataset('organizations.csv')

        set.replace_dataframe(self.users.df)

        self.assertEqual(self.users.df.size, set.df.size)

    def test_df_to_xlsx(self):
        self.orgs.df_to_xlsx('test2')


