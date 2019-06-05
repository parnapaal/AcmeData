import unittest

import pandas as pd


from AcmeData.Dataset import Dataset


class TestDataset(unittest.TestCase):

    def test_open_file_base_case(self):
        #confirm the datasets are being loaded in correctly through pandas by checking the size
        set = Dataset('organizations.csv')
        df = pd.read_csv('organizations.csv')

        self.assertEqual(set.df.size,df.size)

    def test_if_file_not_found_throw_exception(self):

        organization = 'organization.csv'
        set = Dataset(organization)

        self.assertEqual(set.df,"")

    def test_clean_data_base_case(self):
        pass

    def test_clean_data_for_emails(self):
        pass

    def test_clean_data_when_name_is_number(self):
        pass

    def test_clean_data_when_name_is_visitor(self):
        pass
    def if_name_is_just_a_number_flag_it(self):
        pass

    def remove_non_ascii_symbols_during_cleaning(self):
        pass

    def remove_parentheses(self):
        pass

    def remove_quotes(self):
        pass

    def remove_brackets(self):
        pass


    def test_replace_dataframe(self):
        df = pd.read_csv('users.csv')
        set = Dataset('organizations.csv')

        set.replace_dataframe(df)

        self.assertEqual(df.size, set.df.size, msg='our dfs need to be the same size')

    def test_create_hundred_entity_chunks(self):
        pass

    def test_to_json(self, json_fields):
        pass

    def test_upload(self, upload_address):
        pass



