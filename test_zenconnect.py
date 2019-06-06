from unittest import TestCase

from AcmeData.Zenconnect import Zenconnect


class TestZenconnect(TestCase):

    def setUp(self):
        self.z_connect = Zenconnect()


    def test_get_org_list(self):
        self.z_connect.get('organizations')

        pass

    def test_update(self):
        pass

    def test_create_org(self):
        zen_connect = Zendeskconnector(connect_to_where, upload_more_than_one, packet)

    def test_create_many(self):
        pass

