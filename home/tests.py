from django.test import TestCase
from lfainfo22.tests import ClientTestCase

class HomeTest(ClientTestCase):
    def test_access(self):
        self.send_request('/', {})