import enum

from django.core.mail import EmailMessage


class UserType(enum.Enum):
    super_user = 1
    teacher_user = 2
    student_user = 3
    librarian_user = 4