import unittest
from src.domain.assignment import *


class TestAssignment1(unittest.TestCase):
    def setUp(self) -> None:
        self.__asn = Assignment(1, "The toughest.", datetime.datetime.now() + datetime.timedelta(hours=10))

    def test_assignment(self):
        self.assertFalse(self.__asn.is_overdue)

class TestAssignment2(unittest.TestCase):
    def setUp(self) -> None:
        self.__asn = Assignment(1, "The toughest.", datetime.datetime.now() - datetime.timedelta(hours=10))

    def test_assignment(self):
        self.assertTrue(self.__asn.is_overdue)
