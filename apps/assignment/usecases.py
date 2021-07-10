from datetime import datetime

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from apps.assignment.models import Assignment
from apps.materials.models import Material


class AddAssignmentUseCase:
    def __init__(self, serializer, user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._user = user

    def execute(self):
        self._factory()

    def _factory(self):
        self._assignment = Assignment(**self._data, user=self._user)
        self._assignment.save()


class ListAssignmentUseCase:
    def execute(self):
        self._factory()
        return self._assignment

    def _factory(self):
        self._assignment = Assignment.objects.all()


class AssignmentNotFound(NotFound):
    default_detail = _('Assignment  Not found for following id')


class GetAssignmentUseCase:
    def __init__(self, assignment_id):
        self._assignment = assignment_id

    def execute(self):
        self._factory()
        return self.assignment

    def _factory(self):
        try:
            self.assignment = Assignment.objects.get(pk=self._assignment)
        except Assignment.DoesNotExist:
            raise AssignmentNotFound


# class UpdateNoticeUseCase:
class UpdateAssignmentUseCase:
    def __init__(self, serializer, assignment: Assignment):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._assignment = assignment

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            # self._data.get(key)
            setattr(self._assignment, key, self._data.get(key))
        self._assignment.updated_date = datetime.now()
        self._assignment.save()


class DeleteAssignmentUseCase:
    def __init__(self, assignment: Assignment):
        self._assignment = assignment

    def execute(self):
        self._factory()

    def _factory(self):
        self._assignment.delete()
