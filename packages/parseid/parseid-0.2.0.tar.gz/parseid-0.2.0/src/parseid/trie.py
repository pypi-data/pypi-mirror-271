"""
data structure: The trie. Here are the features:
composed by one root node, some parent nodes, and some leave nodes.
one parent nodes could have one or multiple child nodes.
one child node has only one parent node.
leave nodes have not child nodes.

value of root node should be ''
except root node, values of all other nodes should not be None, ''
"""
import sys
from typing import Iterable

from .trie_node import TrieNode


class Trie(object):

    def __init__(self, node_attrs:list=None):
        self.node_attrs = node_attrs
        # One trie has one root node.
        # The root node does not store any character, so val is empty string
        self.root = TrieNode("", self.node_attrs)
        # used for depth-first search recursion
        self.output = []
    
    def insert(self, iter_word:Iterable)->TrieNode:
        """
        Insert a string into the trie
        return reference of the last node
        """
        # start from root
        node = self.root
        for char in iter_word:
            # node.children is dict
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char, self.node_attrs)
                new_node.parent = node
                node.children[char] = new_node
                node = new_node
                self.root.counter += 1
            node.counter += 1
        else:
            node.is_end = True
        # return leave node
        return node
    
    def scan(self, node=None, prefix=None) -> Iterable:
        '''
        recursive: depth-first search
        In default: retrieve all strings stored in Trie
        return: node is leave node
        return: prefix represent  one string stored in Trie
        '''
        if node is None: node = self.root
        if prefix is None: prefix = ''
        if node.is_end:
            yield node, prefix
        for val, child_node in node.children.items():
            yield from self.scan(child_node, prefix + val)

    def dfs_search(self, node, prefix)->tuple:
        """Depth-first search
        node: the node to start with
        prefix: the current prefix-value for this node
        self.output would be updated
        """
        if node.is_end:
            self.output.append((prefix + node.val, node.counter))
        for child in node.children.values():
            self.dfs_search(child, prefix + node.val)
            
    def search(self, iter_prefix:list)->list:
        """
        Retrieve all strings with the same prefix
        for example: prefix=wor, return world, word, words etc.
        """
        # initilize self.output and node
        self.output = []
        node = self.root
        for char in iter_prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        # Traverse all remaining branches to get all candidates
        self.dfs_search(node, iter_prefix[:-1])
        return sorted(self.output, key=lambda x: x[1], reverse=True)
    
    def dump(self)->list:
        '''
        dump all strings to list
        Note: don't do that if numbero of nodes are.
        '''
        # initilize self.output and node
        self.output = []
        node = self.root
        self.dfs_search(node, '')
        return sorted(self.output, key=lambda x: x[0])
            
    def get(self, iter_word:Iterable)->TrieNode:
        """
        exact match a string 
        """
        node = self.root
        word = ''
        for val in iter_word:
            if val in node.children:
                word += val
                node = node.children[val]
            else:
                return None
        else:
            if node.is_end:
                return word
        return None

    def get_node(self, iter_word:Iterable)->TrieNode:
        """
        exact match a string 
        """
        node = self.root
        for val in iter_word:
            if val in node.children:
                node = node.children[val]
            else:
                return None
        else:
            if node.is_end:
                return node
        return None


    def delete(self, iter_word:Iterable)->list:
        """
        delete a node including its children nodes if they exist
        """
        if len(list(iter_word)) == 0:
            return []
        parent = self.root
        node = self.root
        for val in iter_word:
            if val in node.children:
                parent = node
                node = node.children[val]
            else:
                return []
        self.output = []
        self.dfs_search(node, ''.join(iter_word[:-1]))
        del parent.children[val]
        return [a for a,_ in self.output]


    def retrieve(self, node:TrieNode, word:str=None)->str:
        '''
        Given a leave node or parent node in the trie,
        retrieve all parents that could be a string.
        '''
        if type(node).__name__ != 'TrieNode':
            return ''
        if word is None:
            word = ''
        if node.val == '':
            return word
        return self.retrieve(node.parent, node.val+word)

    def insert_relative(self, node:TrieNode, relative_node:TrieNode)->None:
        # connected Trienodes
        if hasattr(node, 'relatives'):
            if relative_node not in node.relatives:
                node.relatives.append(relative_node)
        else:
            node.relatives = [relative_node,]

    
    def get_relatives(self, node:TrieNode)->list:
        if hasattr(node, 'relatives'):
            return node.relatives
        return []
    
    def delete_relatives(self, node:TrieNode)->bool:
        if hasattr(node, 'relatives'):
            delattr(node, 'relatives')
        return False
    
    def memory_size(self):
        size = sys.getsizeof(self.root)
        return  size* self.root.counter
