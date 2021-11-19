from src.domain.validator import Validator, ValidationError


class Grade:
    """ Represents a grade. """
    def __init__(self, assignment_id: int, student_id: int, grade_value: int = 0):
        self.__assignment_id = assignment_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def assignment_id(self):
        return self.__assignment_id

    @assignment_id.setter
    def assignment_id(self, value: int):
        self.__assignment_id = value

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, value: int):
        self.__student_id = value

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, value: int):
        self.__grade_value = value

    @property
    def is_graded(self):
        return self.__grade_value != 0

    def __eq__(self, other):
        return self.assignment_id == other.assignment_id and self.student_id == other.student_id

class GradeValidationError(ValidationError):
    pass

class GradeValidator(Validator):
    """ Provides static methods to validate a grade. """
    @staticmethod
    def validate(grade):
        # check that the grade is between 0 (ungraded) and 10 (max grade)
        if not (grade.grade_value >= 0 or grade.grade_value <= 10):
            raise GradeValidationError("Grade is invalid")
