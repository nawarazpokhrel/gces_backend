from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError, ValidationError
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.db import models
from django.contrib import auth

from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.utils import UserType


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for Management"""
    username_validator = UnicodeUsernameValidator()

    id = ShortUUIDField(
        primary_key=True,
        auto=True,
        editable=False,
    )
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
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

    faculty = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    faculty_code = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    registration_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    parents_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    batch = models.IntegerField(
        help_text=_('This is actually the user or student joined to that institute'),
        null=True,
        blank=True
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.fullname

    def clean(self):
        try:
            domain_list = ["gces.edu.np"]
            email = self.email.rsplit('@')[1]
            # email domain filter
            if not (email in domain_list):
                raise ValidationError(
                    {'email': _('Email can only be created with gces.edu.np  domains try again.')})
        except IndexError:
            raise DjangoValidationError({'email': 'Email is not correct.'})
        todays_date = date.today()

        # Check if joined date is ahead of current date
        # print(int(self.batch) > int(todays_date.year))
        # if self.batch > todays_date.year:
        #     raise DjangoValidationError({'batch': _('Batch  cannot be of future date.')})

    def save(self, *args, **kwargs):
        # be2016se503 @ gces.edu.np
        try:
            if self.is_student:
                self.faculty_code = self.email[6:8]
                self.batch = int(self.email[2:6])
                if self.faculty_code == 'se':
                    self.faculty = 'Software engineering'
                else:
                    self.faculty = 'Computer Engineering'
                self.registration_number = self.email[8:11]
        except IndexError:
            raise DjangoValidationError({'email': 'Email is not correct'})
        super(User, self).save(*args, **kwargs)

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

    @property
    def role(self):
        if self.is_superuser:
            return 'super_user'
        elif self.is_teacher:
            return 'teacher_user'
        elif self.is_student:
            return 'student_user'
        else:
            return 'librarian_user'


class TeacherUserManager(BaseUserManager):
    def get_queryset(self):
        return super(TeacherUserManager, self).get_queryset().filter(

            is_teacher=True,
            is_student=False,
            is_librarian=False,
            is_superuser=False,
        )

    def create(self, **kwargs):
        kwargs.update({

            'is_teacher': True,
            'is_student': False,
            'is_librarian': False,
            'is_superuser': False,
        })
        return super(TeacherUserManager, self).create(**kwargs)


class TeacherUser(User):
    objects = TeacherUserManager()

    class Meta:
        default_permissions = ()
        proxy = True

    def __str__(self):
        return self.fullname

    # def clean(self):
    #     # Check if user is teacher
    #     if not self.user.is_teacher:
    #         raise DjangoValidationError({'user': _('User must be teacher user')})
    #
    #     # Check if joined date is ahead of current date
    #     if self.joined_date > timezone.datetime.now().date():
    #         raise DjangoValidationError({'joined_date': _('Date joined cannot be in future.')})


class StudentUserManager(BaseUserManager):
    def get_queryset(self):
        return super(StudentUserManager, self).get_queryset().filter(

            is_teacher=False,
            is_student=True,
            is_librarian=False,
            is_superuser=False,
        )

    def create(self, **kwargs):
        kwargs.update({

            'is_teacher': False,
            'is_student': True,
            'is_librarian': False,
            'is_superuser': False,
        })
        return super(StudentUserManager, self).create(**kwargs)


class StudentUser(User):
    """
    Proxy model for Student User
    """

    objects = StudentUserManager()

    class Meta:
        default_permissions = ()
        proxy = True

    def __str__(self):
        return self.fullname

    def clean(self):
        # Check if user is student
        if not self.is_student:
            raise DjangoValidationError({'user': _('User must be student user')})


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
        return self.fullname


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
        return self.fullname
