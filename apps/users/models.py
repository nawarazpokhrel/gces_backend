from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.utils import UserType


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for Management"""
    username_validator = UnicodeUsernameValidator()

    id = ShortUUIDField(
        primary_key=True,
        auto=True,
        editable=False,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)
    is_member = models.BooleanField(
        _('member'),
        help_text=_(
            'Designates whether this user should be treated as member. '
        ),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_librarian = models.BooleanField(
        _('librarian status'),
        default=False,
        help_text=_('Designates whether the user is librarian.'),
    )
    is_student = models.BooleanField(
        _('student status'),
        default=False,
        help_text=_('Designates whether the user is student.'),
    )
    is_teacher = models.BooleanField(
        _('teacher status'),
        default=False,
        help_text=_('Designates whether the user is teacher.'),
    )

    is_verified = models.BooleanField(
        _('verification status'),
        default=False,
        help_text=_('Designates whether the user is verified via email or not.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.username

    # def clean(self):
    #     domain_list = ["gces.edu.np"]
    #     email = self.email.rsplit('@')[1]
    #     # email domain filter
    #     if not (email in domain_list):
    #         raise DjangoValidationError(
    #             {'email': _('Email can only be created with gces.edu.np  domains try again.')})

    @property
    def user_type(self):
        if self.is_superuser:
            return UserType.super_user
        elif self.is_teacher:
            return UserType.teacher_user
        elif self.is_student:
            return UserType.student_user
        else:
            return UserType.librarian_user


class TeacherUserManager(BaseUserManager):
    def get_queryset(self):
        return super(TeacherUserManager, self).get_queryset().filter(
            user__is_teacher=True,
            user__is_student=False,
            user__is_librarian=False,
            user__is_superuser=False,
        )

    def create(self, **kwargs):
        kwargs.update({

            'user__is_teacher': True,
            'user__is_student': False,
            'user__is_librarian': False,
            'user__is_superuser': False,
        })
        return super(TeacherUserManager, self).create(**kwargs)


class TeacherUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    faculty = models.CharField(max_length=100)
    faculty_code = models.CharField(max_length=100)
    is_full_time = models.BooleanField(default=False)
    joined_date = models.DateField()

    objects = TeacherUserManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.user.username

    def clean(self):
        # Check if user is teacher
        if not self.user.is_teacher:
            raise DjangoValidationError({'user': _('User must be teacher user')})

        # Check if joined date is ahead of current date
        if self.joined_date > timezone.datetime.now().date():
            raise DjangoValidationError({'joined_date': _('Date joined cannot be in future.')})


class StudentUserManager(BaseUserManager):
    def get_queryset(self):
        return super(StudentUserManager, self).get_queryset().filter(

            user__is_teacher=False,
            user__is_student=True,
            user__is_librarian=False,
            user__is_superuser=False,
        )

    def create(self, **kwargs):
        kwargs.update({

            'user__is_teacher': False,
            'user__is_student': True,
            'user__is_librarian': False,
            'user__is_superuser': False,
        })
        return super(StudentUserManager, self).create(**kwargs)


class StudentUser(BaseModel):
    """
    Proxy model for Student User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    faculty = models.CharField(max_length=100)
    faculty_code = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    parents_name = models.CharField(max_length=100)
    joined_date = models.DateField()

    objects = StudentUserManager()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'registration_number'],
            name='unique_student'
        )
        ]

    def __str__(self):
        return self.user.username

    def clean(self):
        # Check if user is student
        if not self.user.is_student:
            raise DjangoValidationError({'user': _('User must be student user')})

        # Check if joined date is ahead of current date
        if self.joined_date > timezone.datetime.now().date():
            raise DjangoValidationError({'joined_date': _('Date joined cannot be in future.')})


class LibrarianUserManager(BaseUserManager):
    def get_queryset(self):
        return super(LibrarianUserManager, self).get_queryset().filter(
            is_staff=False,
            is_teacher=False,
            is_student=False,
            is_librarian=True,
            is_superuser=False,
        )

    def create(self, **kwargs):
        kwargs.update({
            'is_staff': False,
            'is_teacher': False,
            'is_student': False,
            'is_librarian': True,
            'is_superuser': False,

        })
        return super(LibrarianUserManager, self).create(**kwargs)


class LibrarianUser(User):
    """
    model for Librarian user
    """
    objects = LibrarianUserManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.username


class SystemAdminUserManager(BaseUserManager):
    def get_queryset(self):
        return super(SystemAdminUserManager, self).get_queryset().filter(
            is_staff=True,
            is_teacher=False,
            is_student=False,
            is_librarian=False,
            is_superuser=True
        )

    def create(self, **kwargs):
        kwargs.update({
            'is_teacher': False,
            'is_student': False,
            'is_librarian': False,
            'is_superuser': True,
            'is_staff': True,

        }
        )
        return super(SystemAdminUserManager, self).create(**kwargs)


class SystemAdminUser(User):
    """
    Proxy model for System Admin user
    """
    objects = SystemAdminUserManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.username
