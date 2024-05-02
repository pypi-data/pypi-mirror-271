'''
Test Tree
'''
from .helper import *
from src.parseid import Parse

@ddt
class TestParse(TestCase):

    def test_ditrie(self):
        infile = os.path.join(DIR_DATA, 'gene_refseq_uniprotkb_collab')
        res = Parse(DIR_DATA).map_ncbi_uniprotkb(infile)
        res = [i for i in res['ditrie'].items()]
        assert len(res) == 448595
