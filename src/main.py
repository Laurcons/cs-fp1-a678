from src.domain.assignment import AssignmentValidator
from src.domain.grade import GradeValidator
from src.domain.student import StudentValidator
from src.repository.repository import Repository
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.student_service import StudentService
from src.ui.console import Console

student_repository = Repository(lambda s: s.student_id, StudentValidator)
student_service = StudentService(student_repository)

assignment_repository = Repository(lambda a: a.assignment_id, AssignmentValidator)
assignment_service = AssignmentService(assignment_repository)

grade_repository = Repository(lambda g: (g.assignment_id, g.student_id), GradeValidator)
grade_service = GradeService(grade_repository, assignment_repository, student_repository)

console = Console(student_service, assignment_service, grade_service)
console.start()
