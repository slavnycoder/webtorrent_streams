from django.test import TestCase

from file_storages.google_cloud import gs_client


class GoogleCloudStorageTest(TestCase):

    def test_read_from_cloud(self):
        gs_client.make_private('unit')
