
import unittest

from src.repository.repository import RepositoryError
from src.services.assignment_service import *
import datetime

class TestAssignmentService(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.__std_repo = Repository(lambda x: x.student_id)
        self.__grd_repo = Repository(lambda x: (x.student_id, x.assignment_id))
        self.__asn_repo = Repository(lambda x: x.assignment_id)
        self.__service = AssignmentService(self.__asn_repo, self.__std_repo, self.__grd_repo)

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)
        self.__repo = None
        self.__service = None

    def test_add(self):
        now = datetime.datetime.now()
        self.__service.add_assignment(4, "hello", now)
        self.assertEqual(len(self.__asn_repo.get_all()), 1)
        elem = self.__asn_repo.find_id(4)
        self.assertEqual(elem.assignment_id, 4)
        self.assertEqual(elem.description, "hello")
        self.assertEqual(elem.deadline, now)

    def test_populate(self):
        self.__service.populate()
        self.assertEqual(len(self.__asn_repo.get_all()), 20)

    def test_remove(self):
        self.__service.populate()
        self.__service.remove_assignment(4)
        self.assertEqual(len(self.__asn_repo.get_all()), 19)

        with self.assertRaises(RepositoryError):
            self.__service.remove_assignment(300)

    def test_update(self):
        self.__service.populate()
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        self.__service.add_assignment(21, "hello", now)
        self.__service.update_assignment(21, "no", today)
        asn = self.__asn_repo.find_id(21)

        self.assertEqual(asn.description, "no")
        self.assertEqual(asn.deadline, today)

    def test_get_all(self):
        self.__service.populate()
        self.assertListEqual(self.__service.get_all_assignments(), self.__asn_repo.get_all())

