import unittest

from keepasshttp import util


class TestUtil(unittest.TestCase):
    def testConvertToStr(self):
        self.assertEqual(
            {1: '1', 2: ['2', 'two'], 3: {'3': None}},
            util.convertToStr({1: 1, 2: [2, 'two'], 3: {'3': None}})
        )

    def testMerge(self):
        a = {1: 2, 2: 2}
        b = {1: 1, 3: 3}
        self.assertEqual({1: 1, 2: 2, 3: 3}, util.merge(a, b))
