'''
Test trie
'''
from .helper import *
from src.parseid import DiTrie

@ddt
class TestTrie(TestCase):

    def test_insert(self):
        t = DiTrie()
        # insert one pair
        res = t.insert('ab','xy')
        assert res.val == 'b'
        assert res.relatives[0].val == 'y'

        # insert duplicate
        res = t.insert('ab','xy')
        assert res.counter == 2

    def test_get(self):
        t = DiTrie()
        t.insert('ab','xy')
        
        # correct key
        res = t.get('ab')
        assert res == ['xy']
        # no such a key
        res = t.get('g')
        assert res == []
        # wrong key: empty
        res = t.get('')
        assert res == []

    def test_items(self):
        '''
        test DiTrie().items()
        '''
        t = DiTrie()
        t.insert('ab','xy')
        t.insert('abc','xyz')
        res = [(a,b) for a, b in t.items()]
        assert res == [('ab', ['xy']), ('abc', ['xyz'])]

    def test_switch(self):
        '''
        test DiTrie().switch()
        '''
        t = DiTrie()
        t.insert('ab','xy')
        t.insert('abc','xyz')
        t.switch()
        res = t.get('xy')
        assert res == ['ab']
        res = [(a,b) for a, b in t.items()]
        assert res == [('xy', ['ab']), ('xyz', ['abc'])]