import math
import unittest
import numpy as np
import pandas as pd

from AcmeData.Dataset import Dataset


# Tests for our Dataset class
class TestDataset(unittest.TestCase):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

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



    def test_deal_with_identical_emails(self):
        self.users.dealing_with_identical_emails()


    #flag_aparna() is called on instantiation - we are just checking that the tag is in place
    def test_flagged_as_aparna(self):
        self.assertEqual(self.users.df['tags'][0], 'aparna')

    def test_merging_visitors(self):
        result = pd.concat(g for _, g in self.users.df.groupby("email") if len(g) > 1)
        pass


    #this test is not completely air tight but will work in the case of this one data set clean -- needs to be a bit more
    #airtight in the way assertion statements are picked
    def test_pick_a_merged_subscription(self):
        df = self.users.merge_similar_entries()
        df = self.users.pick_a_merged_subscription(df)
        pass
    #see note above
    def test_pick_a_merged_role(self):
        df = self.users.merge_similar_entries()
        df = self.users.pick_a_merged_role(df)
        #print(df['tags'])
        pass

    def test_dealing_with_identical_emails(self):
        df = self.users.dealing_with_identical_emails()
        df.to_csv('testing_merge.csv')
        #looking_for_alice = self.users.df.loc[self.users.df['name'] == 'Alice']
        #print(looking_for_alice)

    def pass_to_visitors(self):
        pass


    def test_replace_dataframe(self):
        set = Dataset('organizations.csv')

        set.replace_dataframe(self.users.df)

        self.assertEqual(self.users.df.size, set.df.size)

    def test_df_to_xlsx(self):
        self.orgs.df_to_xlsx('test2')


