# parseID: suck, parse identifiers or accession numbers

## Introduction
parseID is a bioinformatics data structure library optimized for sucking identifiers or 
accession numbers into memory, parse those identifiers accession numbers to each other. 

Identifiers or accession numbers are defined and referenced by various biological databases.
Their number could be million size or even billion level.
Some data operations, such as query or parse, are very common.

parseID employs Data structure "trie" and "ditrie". Trie could suck tremendous identifiers into memory at a time. 
Ditrie could suck a large number of mapping of identifiers. Through the trie and ditrie, 
huge data operations including insert, get, search, delete, scan etc could be quickly called.

## testing

```
pytest -s tests
```

## quick start
There is one example about how huge accession numbers are sucked into Trie.
The mapping file could be downloaded from https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_refseq_uniprotkb_collab.gz into local space.
Retrieve 176,513,729 (03/25/2024) UniProt Accession numbers from the file and feed them into Trie.
Showed as the example below, accession numbers are stored in the object uniprotkb_acc_trie. 
```
from parseid import ProcessID
infile = 'gene_refseq_uniprotkb_collab'
uniprotkb_acc_trie = ProcessID(infile).uniprotkb_protein_accession()
```

Retrieve pairs of NCBI protein accession number and UniProt Accession numbers
from file and feed them into Ditrie. Showed as the example below, 
the mapping fo two accession numbers are stored in the object map_trie, 
which is ready for query or parsing.
```
from parseid import ProcessID
infile = 'gene_refseq_uniprotkb_collab'
ncbi_uniprotkb_ditrie = ProcessID(infile).map_ncbi_uniprotkb()
```



