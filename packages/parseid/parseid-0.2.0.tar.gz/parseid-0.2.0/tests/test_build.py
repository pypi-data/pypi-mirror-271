'''
Test Tree
'''
from .helper import *
from src.parseid import Build

@ddt
class TestBuild(TestCase):

    def test_retrieve_ncbi_accession(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        res = Build(DIR_DATA).ncbi_refseq_pacc(infile)
        trie = res['trie'].dump()
        assert len(trie) == 448595
        assert res['records'] == 999999

    def test_retrieve_uniprotkb_accession(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        res = Build().ncbi_uniprotkb_pacc(infile)
        trie = res['trie'].dump()
        assert len(trie) == 822535
        assert res['records'] == 999999


    