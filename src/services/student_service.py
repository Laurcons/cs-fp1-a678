from src.domain.assignment import Assignment
from src.domain.student import Student
from src.domain.student_assignment_grade_dto import StudentAssignmentGradeDTO
from src.domain.student_situation_dto import StudentSituationDTO
from src.repository.repository import Repository

class StudentOperationError(BaseException):
    pass

class StudentService:
    """ Handles operations on the Student repository. """
    def __init__(self, student_repository: Repository, assignment_repository: Repository, grade_repository: Repository):
        self.__student_repository = student_repository
        self.__grade_repository = grade_repository
        self.__assignment_repository = assignment_repository

    def populate(self):
        """ Adds a couple of entries. """
        self.__student_repository.insert_all([
            Student(1, "Pricop Laurentiu", "916"),
            Student(2, "Edward Iakab", "913"),
            Student(3, "Briana Salagean", "916"),
            Student(4, "Mircea Gabriel", "111"),
            Student(5, "Stan Andrei", "916"),
            Student(6, "Bradea Codrin", "435"),
            Student(7, "Pop Codin", "123"),
            Student(8, "Gates Bill", "432"),
            Student(9, "Manole Mesteru", "732"),
            Student(10, "Inca Unu", "123"),
            Student(11, "Pricop Laurentiu 2", "916"),
            Student(12, "Edward Iakab 2", "913"),
            Student(13, "Briana Salagean 2", "916"),
            Student(14, "Mircea Gabriel 2", "111"),
            Student(15, "Stan Andrei 2", "916"),
            Student(16, "Bradea Codrin 2", "435"),
            Student(17, "Pop Codin 2", "123"),
            Student(18, "Gates Bill 2", "432"),
            Student(19, "Manole Mesteru 2", "732"),
            Student(20, "Inca Unu 2", "123"),
        ])

    def add_student(self, student_id, name, group):
        """ Adds a new student. """
        if self.__student_repository.id_exists(student_id):
            raise StudentOperationError("Student id already exists")
        student = Student(student_id, name, group)
        self.__student_repository.add(student)

    def remove_student(self, student_id):
        """ Removes the student, given their id. Returns the removed student. """
        grades = self.__grade_repository.find_all_by_predicate(lambda g: g.student_id == student_id)
        for id_pair in [(g.assignment_id, g.student_id) for g in grades]:
            self.__grade_repository.remove_id(id_pair)
        return self.__student_repository.remove_id(student_id)

    def update_student(self, student_id, name, group):
        """ Updates the data for a student, found by their id. """
        student = self.__student_repository.find_id(student_id)
        student.name = name
        student.group = group
        self.__student_repository.update(student)

    def get_all_students(self):
        """ Returns a list of all the students. """
        return self.__student_repository.get_all()

    def get_all_students_in_group(self, group):
        """ Returns a list of all students that are in a group. """
        return self.__student_repository.find_all_by_predicate(lambda s: s.group == group)

    def get_ungraded_assignments_of_student(self, student_id) -> list[Assignment]:
        """ Returns the ungraded assignments of a student. """
        grades = self.__grade_repository.find_all_by_predicate(lambda g: g.student_id == student_id and not g.is_graded)
        ungraded_ids = [g.assignment_id for g in grades]
        asns = self.__assignment_repository.find_all_by_predicate(lambda a: a.assignment_id in ungraded_ids)
        return asns

    def get_graded_students_for_assignment(self, assignment_id) -> list[StudentAssignmentGradeDTO]:
        """ Gets a list of students, their graded assignments, and the grade for each assignment. """
        grades = self.__grade_repository.find_all_by_predicate(lambda g: g.assignment_id == assignment_id and g.is_graded)
        asn = self.__assignment_repository.find_id(assignment_id)
        out = []
        for grade in grades:
            student = self.__student_repository.find_id(grade.student_id)
            out.append(StudentAssignmentGradeDTO(student, asn, grade))
        out.sort(key=lambda dto: dto.grade.grade_value)
        return out

    def get_students_with_late_assignments(self) -> list[StudentAssignmentGradeDTO]:
        """ Gets a list of students, and their late assignments. """
        asns = self.__assignment_repository.get_all()
        overdue_asns = filter(lambda a: a.is_overdue, asns)
        out = []
        for asn in overdue_asns:
            grades = self.__grade_repository.find_all_by_predicate(lambda g: g.assignment_id == asn.assignment_id and not g.is_graded)
            for grade in grades:
                student = self.__student_repository.find_id(grade.student_id)
                out.append(StudentAssignmentGradeDTO(student, asn, grade))
        return out

    def get_students_with_best_situation(self) -> list[StudentSituationDTO]:
        """ Gets a list of students, along with their average. """
        students = self.__student_repository.get_all()
        out = []
        for student in students:
            grades = self.__grade_repository.find_all_by_predicate(lambda g: g.student_id == student.student_id and g.is_graded)
            if len(grades) == 0:
                continue
            average = 0.0
            for grade in grades:
                average += grade.grade_value
            average /= len(grades)
            out.append(StudentSituationDTO(student, average))
        out.sort(key=lambda dto: dto.average)
        return out
