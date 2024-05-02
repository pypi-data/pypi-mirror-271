"""
data structure: The di-trie. Here are the features:
Define A trie and B trie:
one leave node of A trie is mapped to one or more leave nodes of B trie
"""
from bioomics import NCBI

# from .read_file import ReadFile
from .trie import Trie
from .ditrie import DiTrie

class Process:
    def __init__(self, local_path:str=None):
        self.local_path = local_path
    
    def protein_ncbi_uniprotkb(self) -> DiTrie:
        '''
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        map: UniProtKB accession number ~ NCBI protein accession number
        '''
        # download 
        client = NCBI(self.local_path, overwrite=False)
        local_file = client.download_refseq_uniprotkb()
        print(local_file)
        return None

