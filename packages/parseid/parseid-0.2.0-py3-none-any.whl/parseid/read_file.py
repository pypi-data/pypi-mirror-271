import gzip
import pickle
import os
from typing import Iterable

class ReadFile:

    @staticmethod
    def iter_text(infile, sep:str=None, skip_rows:int=None) -> Iterable:
        # file handler
        handler = gzip.open(infile, 'rt') if infile.endswith('gz') \
            else open(infile, 'r')

        # skip rows if needed
        if skip_rows is None:
            skip_rows = 0
        for n in range(0, skip_rows):
            next(handler)

        # get line by line
        if sep is None:
            for line in handler:
                yield line.rstrip()
        else:
            for line in handler:
                items = line.rstrip().split(sep)
                yield items
        handler.close()

    @staticmethod
    def gene_refseq_uniprotkb_collab(infile:str, col:int=None):
        '''
        read "gene_refseq_uniprotkb_collab" downloaded from NCBI
        '''
        # if self.infile is None:
        #     self.infile = os.path.join(local_path, 'NCBI', 'refseq', 'gene_refseq_uniprotkb_collab.gz')
        if os.path.isfile(infile):
            records = ReadFile.iter_text(infile, sep='\t', skip_rows=1)
            if col is None:
                for items in records:
                    yield items
            else:
                for items in records:
                    yield items[col]
        else:
            print("no such a file")

    @staticmethod
    def load_data(infile:str=None):
        try:
            if os.path.isfile(infile):
                with open(infile, 'rb') as f:
                    data = pickle.load(f)
                    return data
        except Exception as e:
            print(f"Failed in read data from {infile}. error={e}")


    @staticmethod
    def dump_data(data, outfile:str) -> bool:
        try:
            with open(outfile, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Failed in saving {outfile} in pickle format. error={e}")
        return False