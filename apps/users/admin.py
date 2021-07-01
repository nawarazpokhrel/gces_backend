from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users import models, forms

User = get_user_model()


class BaseUserAdmin(UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = (
        'id',
        'fullname',
        'phone_number',
        'is_superuser',
        'is_student',
        'is_teacher',
        'batch',
    )
    search_fields = (
        'id',
        'email',
        'phone_number'
    )
    list_display_links = ('id',)

    list_filter = (
        'is_active',
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'phone_number',
            'fullname',

        )}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                'is_student', 'is_teacher', 'is_librarian', 'is_verified',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.LibrarianUser)
class LibrarianUserAdmin(BaseUserAdmin):
    add_form = forms.LibrarianUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'phone_number',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_librarian', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.StudentUser)
class StudentUserAdmin(BaseUserAdmin):
    add_form = forms.StudentUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'phone_number',
            'faculty',
            'faculty_code',
            'registration_number',
            'parents_name',
            'batch',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_student', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.TeacherUser)
class TeacherUserAdmin(BaseUserAdmin):
    add_form = forms.TeacherUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'phone_number',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_teacher', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = (
        'is_active',
        'is_teacher',
    )


@admin.register(models.SystemAdminUser)
class SystemUserAdmin(BaseUserAdmin):
    add_form = forms.SystemAdminUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            # 'email',
            'phone_number',
        )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',)
