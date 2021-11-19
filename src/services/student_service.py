from src.domain.student import Student
from src.repository.repository import Repository

class StudentOperationError(BaseException):
    pass

class StudentService:
    """ Handles operations on the Student repository. """
    def __init__(self, student_repository: Repository):
        self.__student_repository = student_repository

    def populate(self):
        """ Adds a couple of entries. """
        self.__student_repository.insert_all([
            Student(1, "Pricop Laurentiu", "916"),
            Student(2, "Edward Iakab", "913"),
            Student(3, "Briana Salagean", "916"),
            Student(4, "Mircea Gabriel", "111"),
            Student(5, "Stan Vlad", "916"),
            Student(6, "Bradea Codrin", "435"),
            Student(7, "Pop Codin", "123"),
            Student(8, "Gates Bill", "432"),
            Student(9, "Manole Mesteru", "732"),
            Student(10, "Inca Unu", "123"),
            Student(11, "Pricop Laurentiu 2", "916"),
            Student(12, "Edward Iakab 2", "913"),
            Student(13, "Briana Salagean 2", "916"),
            Student(14, "Mircea Gabriel 2", "111"),
            Student(15, "Stan Vlad 2", "916"),
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
        self.__student_repository.insert_or_update(student)

    def remove_student(self, student_id):
        """ Removes the student, given their id. Returns the removed assignment. """
        return self.__student_repository.remove_id(student_id)

    def update_student(self, student_id, name, group):
        """ Updates the data for a student, found by their id. """
        student = self.__student_repository.find_id(student_id)
        student.name = name
        student.group = group
        self.__student_repository.insert_or_update(student)

    def get_all_students(self):
        """ Returns a list of all the students. """
        return self.__student_repository.get_all()

    def get_all_students_in_group(self, group):
        """ Returns a list of all students that are in a group. """
        return self.__student_repository.find_all_by_predicate(lambda s: s.group == group)
