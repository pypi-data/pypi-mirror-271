"""
data structure: The trie. Here are the features:
composed by one root node, some parent nodes, and some leave nodes.
one parent nodes could have one or multiple child nodes.
one child node has only one parent node.
leave nodes have not child nodes.

value of root node should be ''
except root node, values of all other nodes should not be None, ''
"""

class TrieNode:
    """A node in the trie structure"""
    def __init__(self, val:str, node_attrs:list=None):
        self.val = str(val)
        # child nodes: keys are child.val, values are child nodes
        self.children = {}
        # parent node: only one node in TireNode type
        self.parent = None
        # is the end of a string. may or may not be leave node
        self.is_end = False
        #Optional: count number of duplicated strings
        self.counter = 0
        #Optional: attributes of this node
        if isinstance(node_attrs, list):
            for a,v in node_attrs:
                setattr(self, a, v)

    @property
    def is_leave(self):
        '''
        only leave node is True
        '''
        return False if self.children else True
    
    @property
    def is_root(self):
        '''
        only root node has no parent
        Usually the value of the root is empty string
        '''
        return True if self.parent is None else False

    def append(self, new_val):
        if new_val in self.children:
            return self.children[new_val]
        # create new node
        new_node = TrieNode(new_val)
        new_node.parent = self
        self.children[new_val] = new_node
        return new_node
        
