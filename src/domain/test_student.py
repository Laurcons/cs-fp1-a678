import unittest

from src.domain.student import Student, StudentValidator, StudentValidationError


class TestStudent1(unittest.TestCase):
    def setUp(self) -> None:
        self.__student = Student(1, "Martin Luther King", "916")

    def test_student(self):
        StudentValidator.validate(self.__student) # passes
        self.assertEquals(self.__student.specialization, "IE")
        self.assertEquals(self.__student.year, "1")

class TestStudent2(unittest.TestCase):
    def setUp(self) -> None:
        self.__student = Student(2, "Edward Iakab gg wp", "933")

    def test_student(self):
        StudentValidator.validate(self.__student)
        self.assertEquals(self.__student.year, "3")

class TestStudent3(unittest.TestCase):
    def setUp(self) -> None:
        self.__student = Student(3, "who tf", "143")

    def test_student(self):
        with self.assertRaises(StudentValidationError) as re:
            StudentValidator.validate(self.__student)
        self.assertEquals(str(re.exception), "Group is invalid")
