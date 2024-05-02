'''
Test ENV
'''
from .helper import *


@ddt
class TestENV(TestCase):

    def setUp(self):
        pass

    def test_env(self):
        print(DIR_TESTS)
        print(DIR_DATA)
        print(DIR_RESULTS)