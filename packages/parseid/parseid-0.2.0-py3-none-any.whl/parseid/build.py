'''
Build trie of IDs
'''

import os

from .read_file import ReadFile
from .trie import Trie

class Build:
    def __init__(self, local_path:str=None):
        self.local_path = local_path
        self.save = True if local_path and os.path.isdir(local_path) else False
        self.meta = {'records': 0, 'trie': None}


    def ncbi_refseq_pacc(self, infile:str) -> dict:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck NCBI protein accepython setup.pyssion numbers
        """
        acc_trie = Trie()
        acc_iter = ReadFile.gene_refseq_uniprotkb_collab(infile, col=0)
        for acc in acc_iter:
            acc_trie.insert(acc)
            self.meta['records'] += 1
        self.meta['trie'] = acc_trie
        # save trie
        if self.save:
            outfile = os.path.join(self.local_path, 'ncbi_refseq_protein_accession.trie')
            ReadFile.dump_data(acc_trie, outfile)
            self.meta['pickle_file'] = outfile
        return self.meta
    
    def ncbi_uniprotkb_pacc(self, infile:str) -> dict:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck UniProtKB protein accession numbers
        """
        acc_trie = Trie()
        acc_iter = ReadFile.gene_refseq_uniprotkb_collab(infile, 1)
        for acc in acc_iter:
            acc_trie.insert(acc)
            self.meta['records'] += 1
        self.meta['trie'] = acc_trie
        return self.meta

