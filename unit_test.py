# coding=utf8
import unittest
from exp1 import Term
from exp1_refa_for_lab6 import Solution


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.term = Term()
        print "Set up now!"

    def test1(self):
        self.assertEqual(self.term)
