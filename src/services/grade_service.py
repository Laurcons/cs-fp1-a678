from src.domain.grade import Grade
from src.repository.repository import Repository

class GradeOperationError(BaseException):
    pass

class GradeService:
    """ Handles operations on the Grades repository. """
    def __init__(self, grade_repository: Repository, assignment_repository: Repository, student_repository: Repository):
        self.__grade_repository = grade_repository
        self.__student_repository = student_repository
        self.__assignment_repository = assignment_repository

    def assign_to_student(self, assignment_id, student_id):
        """ Assigns an assignment to a student. """
        if not self.__assignment_repository.id_exists(assignment_id):
            raise GradeOperationError("Assignment id doesn't exist")
        if not self.__student_repository.id_exists(student_id):
            raise GradeOperationError("Student id doesn't exist")
        grade = Grade(assignment_id, student_id, 0)
        self.__grade_repository.add(grade)

    def assign_to_group(self, assignment_id, group):
        """ Assigns an assignment to a group of students. """
        students = self.__student_repository.find_all_by_predicate(lambda s: s.group == group)
        for stud in students:
            self.assign_to_student(assignment_id, stud.student_id)

    def get_all_assignations(self):
        """ Returns a list of all the assignations. """
        return self.__grade_repository.get_all()

    def apply_grade_to_student(self, assignment_id, student_id, grade_value):
        """ Applies a grade to a student. If already applied, raises GradeOperationError. """
        if not self.__assignment_repository.id_exists(assignment_id):
            raise GradeOperationError("Assignment id doesn't exist")
        if not self.__student_repository.id_exists(student_id):
            raise GradeOperationError("Student id doesn't exist")
        grade = self.__grade_repository.find_id((assignment_id, student_id))
        if grade.grade_value != 0:
            raise GradeOperationError("Assignment already graded")
        grade.grade_value = grade_value
        self.__grade_repository.update(grade)
