import unittest

from Common.Common import *

class Test_Common(unittest.TestCase):
    """Тестирование общих методов разделяемых всеми функциями и классами приложения"""

    def test_LPair(self):
        """Тестирование получения левой части валютной пары"""
        self.assertTrue(LPair('BTC_USD') == 'BTC')

    def test_RPair(self):
        """Тестирование получения правой части валютной пары"""
        self.assertTrue(RPair('BTC_USD') == 'USD')

    def test_dictKeysRename(self):
        """Тестирование функции переименования ключей словаря"""
        testDict = {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}}
        self.assertTrue(dictKeysRename(testDict, 'A', 'C') == {'C' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRename(testDict, 'C', 'A') == {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRename(testDict, ['A', 'B'], ['C', 'D']) == {'C' : {'a' : 1, 'b' : 2}, 'D' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRename(testDict, ['C', 'D'], ['A', 'B']) == {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRename(testDict['A'], 'a', 'c') == {'c' : 1, 'b' : 2})
        self.assertTrue(testDict == {'A' : {'c' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRename(testDict['A'], 'c', 'a') == {'a' : 1, 'b' : 2})
        self.assertTrue(testDict == {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})

    def test_dictKeysRemove(self):
        """Тестирование функции удаления ключей словаря"""
        testDict = {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}}
        self.assertTrue(dictKeysRemove(dict(testDict), 'A') == {'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRemove(dict(testDict), 'B') == {'A' : {'a' : 1, 'b' : 2}})
        self.assertTrue(dictKeysRemove(dict(testDict), ['A', 'B']) == {})
        self.assertTrue(dictKeysRemove(dict(testDict), ['A', 'B', 'C']) == None)
        self.assertTrue(dictKeysRemove(dict(testDict), ['B', 'C']) == None)
        self.assertTrue(dictKeysRemove(dict(testDict), ['C']) == None)
        self.assertTrue(dictKeysRemove(dict(testDict), 'C') == None)
        self.assertTrue(dictKeysRemove(testDict, 'A') == {'B' : {'c' : 2, 'd' : 4}})
        self.assertTrue(dictKeysRemove(testDict, 'B') == {})
        testDict = {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}}
        self.assertTrue(dictKeysRemove(testDict['A'], 'a') == {'b' : 2})
        self.assertTrue(testDict == {'A' : {'b' : 2}, 'B' : {'c' : 2, 'd' : 4}})
        testDict = {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}}
        self.assertTrue(dictKeysRemove(testDict['B'], ['c', 'd']) == {})
        self.assertTrue(testDict == {'A' : {'a' : 1, 'b' : 2}, 'B' : {}})
        testDict = {'A' : {'a' : 1, 'b' : 2}, 'B' : {'c' : 2, 'd' : 4}}
        self.assertTrue(dictKeysRemove(testDict['A'], ['a', 'b']) == {})
        self.assertTrue(dictKeysRemove(testDict['B'], ['c', 'd']) == {})
        self.assertTrue(testDict == {'A' : {}, 'B' : {}})
        self.assertTrue(dictKeysRemove(testDict, ['A', 'B']) == {})
        self.assertTrue(testDict == {})

    def test_dictValuesToFloat(self):
        testDict = {'A': {'a': '1', 'b': '2'}, 'B': {'c': '3', 'd': '4'}}
        self.assertTrue(dictValuesToFloat(testDict['A']) == {'a': 1, 'b': 2})
        self.assertTrue(dictValuesToFloat(testDict['B']) == {'c': 3, 'd': 4})
        self.assertTrue(dictValuesToFloat(testDict['A']) == {'a': 1, 'b': 2})
        self.assertTrue(dictValuesToFloat(testDict['B']) == {'c': 3, 'd': 4})
        testDict = {'A': {'a': 'a', 'b': 'b'}, 'B': {'c': 'c', 'd': 'd'}}
        self.assertTrue(dictValuesToFloat(testDict['A']) == None)
        self.assertTrue(dictValuesToFloat(testDict['B']) == None)
        self.assertTrue(dictValuesToFloat(testDict) == None)

if __name__ == '__main__':
    unittest.main()
