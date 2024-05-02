'''
Test Tree
'''
from .helper import *
from src.parseid import Process

@ddt
class TestProcess(TestCase):

    def test_retrieve_uniprotkb_accession(self):
        uniprotkb_acc_trie = Process(DIR_DATA).protein_ncbi_uniprotkb()

