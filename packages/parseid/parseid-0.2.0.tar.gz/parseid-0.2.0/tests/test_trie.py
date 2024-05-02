'''
Test trie
'''
from .helper import *
from src.parseid import Trie

@ddt
class TestTrie(TestCase):

    @data(
        [['w', 'wo', 'wolf'], ['w', 'wo', 'wolf']],
        [['abc', 'abc'], ['abc']],
        [['abc',], ['abc']],
        [[], []],
    )
    @unpack
    def test_insert(self, input, expect):
        t = Trie()
        for s in input:
            t.insert(s)
        res = [a for _,a in t.scan()]
        assert res == expect

    @data(
        # only prefix matching
        ['wo', [('word', 2), ('wolf', 2), ('words', 1)]],
        ['word', [('word', 2),('words', 1),]],
        # middle or tail matching is not working
        ['or', []],
        ['lf', []],
    )
    @unpack
    def test_search(self, input ,expect):
        t = Trie()
        for s in ['word', 'words', 'fox', 'wolf', 'wolf']:
            t.insert(s)
        res = t.search(input)
        assert res == expect

    def test_dump(self):
        t = Trie()
        t.insert(list('word'))
        t.insert(list('words'))
        t.insert(list('world'))
        t.insert(list('wolf'))
        t.insert(list('wolf'))
        t.insert(list('golf'))
        res = t.dump()
        expect = [('golf', 1), ('wolf', 2), ('word', 2), ('words', 1), ('world', 1)]
        assert res == expect

    def test_scan(self):
        '''
        root
        / \
       g   w
       |   |
       o   o
       |   |\
       l   l r
       |   | |\
       f   f d l
             | |
             s d
        '''
        t = Trie()
        res = [a for a,_ in t.scan()]
        assert res == []

        t.insert(list('word'))
        t.insert(list('words'))
        t.insert(list('world'))
        t.insert(list('wolf'))
        t.insert(list('wolf'))
        t.insert(list('golf'))
        words = []
        leave_word = []
        for node, prefix in t.scan():
            words.append(prefix)
            leave_word.append(node.val)
        assert words == ['word', 'words', 'world', 'wolf', 'golf']
        assert leave_word == ['d', 's', 'd', 'f', 'f']

    def test_get(self):
        t = Trie()
        res = t.get('wo')
        assert res is None
        t.insert(list('word'))
        t.insert(list('words'))
        res = t.get('wo')
        assert res is None
        res = t.get('')
        assert res is None

        res = t.get('word')
        assert res == 'word'
        res = t.get('words')
        assert res == 'words'

    def test_get_node(self):
        t = Trie()
        res = t.get_node('wo')
        assert res is None
        t.insert(list('word'))
        t.insert(list('words'))
        res = t.get_node('wo')
        assert res is None
        res = t.get_node('')
        assert res is None

        res = t.get_node('word')
        assert getattr(res, 'val') == 'd'
        res = t.get_node('words')
        assert getattr(res, 'val') == 's'
        res = t.get_node('wordss')
        assert res is None

    def test_delete(self):
        t = Trie()
        res = t.delete('wo')
        assert res == []
        t.insert(list('word'))
        t.insert(list('words'))
        res = t.delete('wordss')
        assert res == []
        res = t.delete('')
        assert res == []
        res = t.delete('f')
        assert res == []

        t.insert(list('w'))
        t.insert(list('golf'))
        res = t.delete('wo')
        assert res ==  ['word', 'words']
        res = t.dump()
        assert res == [('golf', 1), ('w', 3)]
        res = t.delete('w')
        assert res ==  ['w',]
        res = t.dump()
        assert res == [('golf', 1)]


    def test_retrieve(self):
        t = Trie()
        res = t.retrieve(t.root)
        assert res == ''
        res = t.retrieve(None)
        assert res == ''
        res = t.retrieve('abc')
        assert res == ''

        last_node = t.insert('word')
        res = t.retrieve(last_node)
        assert res == 'word'

        last_node = t.insert('wo')
        res = t.retrieve(last_node)
        assert res == 'wo'
    
    def test_relative(self):
        t = Trie()
        node = t.insert(list('word'))
        node_a = t.insert(list('truck'))
        node_b = t.insert(list('car'))
        t.insert_relative(node, node_a)
        t.insert_relative(node, node_b)
        relatives = t.get_relatives(node)
        res = [i.val for i in relatives]
        assert res == ['k', 'r']
        res = [t.retrieve(i) for i in relatives]
        assert res == ['truck', 'car']


    def test_memory_size(self):
        t = Trie()
        t.insert(list('word'))
        t.insert(list('words'))
        t.insert(list('world'))
        t.insert(list('wolf'))
        t.insert(list('wolf'))
        t.insert(list('golf'))
        t.insert(list('abc')*100)
        res = t.memory_size()
        assert res > 15072