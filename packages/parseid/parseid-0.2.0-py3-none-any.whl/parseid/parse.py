"""
data structure: The di-trie. Here are the features:
Define A trie and B trie:
one leave node of A trie is mapped to one or more leave nodes of B trie
"""
import os

from .read_file import ReadFile
from .trie import Trie
from .ditrie import DiTrie

class Parse:
    def __init__(self, local_path:str=None):
        self.local_path = local_path
        self.save = True if local_path and os.path.isdir(local_path) else False
        self.meta = {'records':0}
    def map_ncbi_uniprotkb(self, infile) -> DiTrie:
        '''
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        map: UniProtKB accession number ~ NCBI protein accession number
        '''
        uniprotkb_acc_trie = Trie()
        ncbi_acc_trie = Trie()
        map_trie = DiTrie(uniprotkb_acc_trie, ncbi_acc_trie)

        records = ReadFile.gene_refseq_uniprotkb_collab(infile)
        for items in records:
            ncbi_acc, uniprotkb_acc = items[:2]
            map_trie.insert(ncbi_acc, uniprotkb_acc)
            self.meta['records'] += 1
        self.meta['ditrie'] = map_trie

        # save trie
        if self.save:
            outfile = os.path.join(self.local_path, 'ncbi_refseq_vs_uniprotkb_protein_accession.ditrie')
            ReadFile.dump_data(map_trie, outfile)
            self.meta['pickle_file'] = outfile
        return self.meta
    

