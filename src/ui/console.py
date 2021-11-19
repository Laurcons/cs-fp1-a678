import datetime

from src.services.assignment_service import AssignmentService, AssignmentOperationError
from src.services.grade_service import GradeService, GradeOperationError
from src.services.student_service import StudentService, StudentOperationError


class Console:
    """ Handles interaction between the Services and the Human. """
    def __init__(self,
                 student_service: StudentService,
                 assignment_service: AssignmentService,
                 grade_service: GradeService):
        self.__student_service = student_service
        self.__assignment_service = assignment_service
        self.__grade_service = grade_service
        self.__student_service.populate()
        self.__assignment_service.populate()

    def __handle_assignment_add(self):
        print("Let's add an assignment together.\n")
        assignment_id = int(input("Assignment id: ").strip())
        description = input("Description: ").strip()
        deadline = input("Deadline, in ISO format: ").strip()
        try:
            deadline = datetime.datetime.fromisoformat(deadline)
            self.__assignment_service.add_assignment(assignment_id, description, deadline)
        except ValueError:
            print("Invalid date!")
        except AssignmentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignment_remove(self):
        print("Let's remove an assignment together!\n")
        assignment_id = int(input("Assignment id: ").strip())
        try:
            self.__assignment_service.remove_assignment(assignment_id)
        except AssignmentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignment_update(self):
        print("Let's update an assignment together!\n")
        assignment_id = int(input("Assignment id: ").strip())
        description = input("Description: ").strip()
        deadline = input("Deadline, in ISO format: ").strip()
        try:
            deadline = datetime.datetime.fromisoformat(deadline)
            self.__assignment_service.update_assignment(assignment_id, description, deadline)
        except ValueError:
            print("Invalid date!")
        except AssignmentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignment_list(self):
        print("All assignments:\n")
        try:
            asns = self.__assignment_service.get_all_assignments()
            for asn in asns:
                print(asn)
        except AssignmentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_student_add(self):
        print("Let's add a student together.\n")
        student_id = int(input("Student id: ").strip())
        name = input("Name: ").strip()
        group = input("Group: ").strip()
        try:
            self.__student_service.add_student(student_id, name, group)
        except StudentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_student_remove(self):
        print("Let's remove a student together.\n")
        student_id = int(input("Student id: ").strip())
        try:
            self.__student_service.remove_student(student_id)
        except StudentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_student_update(self):
        print("Let's update a student together.\n")
        student_id = int(input("Student id: ").strip())
        name = input("Name: ").strip()
        group = input("Group: ").strip()
        try:
            self.__student_service.update_student(student_id, name, group)
        except StudentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_student_list(self):
        print("All students:\n")
        try:
            studs = self.__student_service.get_all_students()
            for stud in studs:
                print(stud)
        except StudentOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignations_to_student(self):
        student_id = int(input("The student id to assign to: ").strip())
        assignment_id = int(input("The assignment id to assign: ").strip())
        try:
            self.__grade_service.assign_to_student(assignment_id, student_id)
        except GradeOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignations_to_group(self):
        group = input("The group to assign to: ").strip()
        assignment_id = int(input("The assignment id to assign: ").strip())
        try:
            self.__grade_service.assign_to_group(assignment_id, group)
        except GradeOperationError as e:
            print(f"Something went wrong: {e}")

    def __handle_assignations_list(self):
        print("All assignations:")
        try:
            assns = self.__grade_service.get_all_assignations()
            for assn in assns:
                print(f"Asn. #{assn.assignment_id} for stud #{assn.student_id}: {'ungraded' if not assn.is_graded else assn.grade_value}")
        except GradeOperationError as e:
            print(f"Something went wrong: {e}")

    def __run_suboptions(self, suboptions: dict, prompt: str):
        print(prompt)
        subopt = input("Choose: ")
        if subopt == 'e': return
        subopt = int(subopt)
        # execute
        try:
            suboptions[subopt]()
        except BaseException as e:
            print(f"Something has happened. Try again? {e}")

    def __print_menu(self):
        print("\nThe Student Assignment Manager (SAM). What do you want to do?\n"
              "1. Modify assignments\n"
              "2. Modify students\n"
              "3. Modify assignations\n"
              # "3. Assign to a student\n"
              # "4. Assign to a group\n"
              "x. Exit\n")

    def __get_assignments_menu_prompt(self):
        return "What do you want to do?\n" \
               "1. Add an assignment\n" \
               "2. Remove an assignment\n" \
               "3. Update an assignment\n" \
               "4. List all assignments\n" \
               "e. Back\n"

    def __get_students_menu_prompt(self):
        return "What do you want to do?\n" \
               "1. Add a student\n" \
               "2. Remove a student\n" \
               "3. Update a student\n" \
               "4. List all students\n" \
               "e. Back\n"

    def __get_assignations_menu_prompt(self):
        return "What do you want to do?\n" \
               "1. Assign to student\n" \
               "2. Assign to group\n" \
               "3. View all assignations\n" \
               "e. Back\n"

    def start(self):
        options = {
            1: lambda: self.__run_suboptions({
                1: self.__handle_assignment_add,
                2: self.__handle_assignment_remove,
                3: self.__handle_assignment_update,
                4: self.__handle_assignment_list,
            }, self.__get_assignments_menu_prompt()),
            2: lambda: self.__run_suboptions({
                1: self.__handle_student_add,
                2: self.__handle_student_remove,
                3: self.__handle_student_update,
                4: self.__handle_student_list,
            }, self.__get_students_menu_prompt()),
            3: lambda: self.__run_suboptions({
                1: self.__handle_assignations_to_student,
                2: self.__handle_assignations_to_group,
                3: self.__handle_assignations_list,
            }, self.__get_assignations_menu_prompt())
        }
        while True:
            self.__print_menu()
            option = input("Choose: ")
            if option == 'x':
                break
            option = int(option)
            options[option]()
