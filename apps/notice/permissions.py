from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_teacher and request.user.is_authenticated)


class IsLibrarian(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_librarian and request.user.is_authenticated)
