'''
Test trie
'''
from .helper import *
from src.parseid import TrieNode

@ddt
class TestTrieNode(TestCase):

    @data(
        ['', ''],
        [3, '3'],
        ['a', 'a'],
    )
    @unpack
    def test_value(self, val, expect):
        node = TrieNode(val)
        assert node.val == expect
    
    def test_tree(self):
        root = TrieNode('')
        node1 = root.append('a')
        node2 = node1.append('b')

        assert root.children == {'a': node1}
        assert node1.children == {'b': node2}
        assert node2.children == {}

        assert root.parent is None
        assert node1.parent == root
        assert node2.parent == node1

        assert root.is_leave is False
        assert node1.is_leave is False
        assert node2.is_leave is True

        assert root.is_root is True
        assert node1.is_root is False
        assert node2.is_root is False

    @data(
        ['a', 56],
        ['0', 56],
    )
    @unpack
    def test_node_size(self, val, expect):
        node = TrieNode(val)
        assert sys.getsizeof(node) == expect
