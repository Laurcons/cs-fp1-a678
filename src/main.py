
from src.repository.repository import Repository
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.student_service import StudentService
from src.ui.console import Console

student_repository = Repository(lambda s: s.student_id)
assignment_repository = Repository(lambda a: a.assignment_id)
grade_repository = Repository(lambda g: (g.assignment_id, g.student_id))

grade_service = GradeService(grade_repository, assignment_repository, student_repository)
student_service = StudentService(student_repository, assignment_repository, grade_repository)
assignment_service = AssignmentService(assignment_repository, student_repository, grade_repository)

console = Console(student_service, assignment_service, grade_service)
console.start()
