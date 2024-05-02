"""
data structure: The di-trie. Here are the features:
Define A trie and B trie:
one leave node of A trie is mapped to one or more leave nodes of B trie
"""
from typing import Iterable
from .trie_node import TrieNode
from .trie import Trie

class DiTrie(object):

    def __init__(self, atrie:Trie=None, btrie:Trie=None):
        self.atrie = atrie if atrie else Trie()
        self.btrie = btrie if btrie else Trie()
    
    def insert(self, a_iter:Iterable, b_iter:Iterable) -> TrieNode:
        '''
        insert key-value into atrie and btrie, respectively
        '''
        a_node = self.atrie.insert(a_iter)
        b_node = self.btrie.insert(b_iter)
        self.atrie.insert_relative(a_node, b_node)
        return a_node
    
    def get(self, a_iter:Iterable) -> list:
        '''
        give key in atrie, get value in btrie
        '''
        output = []
        end_node = self.atrie.get_node(a_iter)
        if end_node:
            for relative_node in self.atrie.get_relatives(end_node):
                word = self.btrie.retrieve(relative_node)
                if word and word not in output:
                    output.append(word)
        return output

    def items(self) -> Iterable:
        '''
        scan the two trie, return pair of key-value
        '''
        for end_node, prefix in self.atrie.scan():
            values = []
            for relative_node in self.atrie.get_relatives(end_node):
                word = self.btrie.retrieve(relative_node)
                if word and word not in values:
                    values.append(word)
            yield (prefix, values)
    
    def switch(self):
        '''
        switch key-values
        '''
        for end_node, _ in self.atrie.scan():
            for relative_node in self.atrie.get_relatives(end_node):
                self.btrie.insert_relative(relative_node, end_node)
            self.atrie.delete_relatives(end_node)
        self.atrie, self.btrie = self.btrie, self.atrie
