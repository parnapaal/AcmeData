import math
import unittest

import pandas as pd


from AcmeData.Dataset import Dataset


class TestDataset(unittest.TestCase):

    def setUp(self):
        self.orgs = Dataset('organizations.csv')
        self.users = Dataset('users.csv')
        self.tickets = Dataset('tickets.csv')

    def tearDown(self):
        self.orgs = None
        self.users = None
        self.tickets = None



    def test_open_file_base_case(self):
        #confirm the datasets are being loaded in correctly through pandas by checking the size

        df = pd.read_csv('organizations.csv')

        self.assertEqual(self.orgs.df.size, df.size)

    def test_if_file_not_found_throw_exception(self):

        organization = 'organization.csv'
        set = Dataset(organization)


        self.assertTrue(set.df == "")

    def test_clean_data_base_case(self):
        pass

    def test_clean_data_when_name_is_number(self):
        pass

    def if_name_is_just_a_number_flag_it(self):
        pass

    def remove_non_ascii_symbols_during_cleaning(self):
        pass

    def test_replace_dataframe(self):
        set = Dataset('organizations.csv')

        set.replace_dataframe(self.users.df)

        self.assertEqual(self.users.df.size, set.df.size, msg='our dfs need to be the same size')

    def test_create_hundred_entity_chunks_base(self):
        df = pd.read_csv('organizations.csv')
        num_dfs = math.ceil(len(df.index)/100)

        df_array = self.orgs.create_hundred_entity_chunks()

        self.assertEqual(num_dfs,len(df_array))

    def test_create_hundred_entity_chunks_bigger_sets(self):

        df = pd.read_csv('tickets.csv')
        num_dfs = math.ceil(len(df.index) / 100)

        df_array = self.tickets.create_hundred_entity_chunks()

        self.assertEqual(num_dfs, len(df_array))

    def test_to_json_format_for_orgs(self):
        string_should_be = {"name": "1,000 Bulbs", "domain_names": ['1000bulbs.com'], "details": "", "notes": "", "organization_fields":{"region": "apac"}, "tags": ['']}
        #there is an intentional mismatch between "tags":[''] and "tags":[""] to ensure they would still mean the same
        #value

        val = ["1,000 Bulbs", ["1000bulbs.com"], "", "", "apac", [""]]
        string_is = self.orgs.to_json_format(val, 'organization')

        self.assertEqual(string_is, string_should_be)

    def test_to_json_format_for_orgs_with_multiple_array_values(self):
        string_should_be = {"name": "1,000 Bulbs", "domain_names": ['1000bulbs.com', 'protonmail.com'], "details": "", "notes": "", "tags": ['vip'], "organization_fields":{"region": "apac"}}

        val = ["1,000 Bulbs", ['1000bulbs.com','protonmail.com'], "", "", "apac", ['vip']]

        string_is = self.orgs.to_json_format(val, 'organization')
        self.assertEqual(string_is,string_should_be)

    def test_to_json_format_orgs_with_no_org_fields(self):
        string_should_be = {"name": "1,000 Bulbs", "domain_names": ['1000bulbs.com', 'protonmail.com'], "details": "", "notes": "", "tags": ['vip']}


        val = ["1,000 Bulbs", ['1000bulbs.com', 'protonmail.com'], "", "", "", ['vip']]

        string_is = self.orgs.to_json_format(val, 'organization')

        self.assertEqual(string_is, string_should_be)


    def test_to_json_format_users(self):
        string_should_be = {
      "name": "Jennifer Hansen",
      "email": "jhansen@example.com",
      "organization_id": 366775269013,
      "role": "admin",
      "tags": [''],
      "active": "true",
      "shared": "false",
      "shared_agent": "false",
      "notes": '',
      "default_group_id": 360004465953,
      "user_fields": {
          "employee_id":"",
          "promotion_code": "doloratdoloremque",
          "subscription": "plan_gold",
      }}
        val = ["Jennifer Hansen", "jhansen@example.com", 366775269013, "admin",[''], "true", "false", "false", '',
               360004465953, '', "doloratdoloremque", "plan_gold"]

        string_is = self.users.to_json_format(val,'users')


        self.assertEqual(string_is, string_should_be)

    def test_to_json_format_tickets(self):
        pass


    def test_upload(self):
        pass



