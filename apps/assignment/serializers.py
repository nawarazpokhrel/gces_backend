from rest_framework import serializers

from apps.assignment.models import Assignment
from apps.materials.models import Material
from gces_backend import settings


class AssignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AddAssignmentSerializers(AssignmentSerializers):
    class Meta(AssignmentSerializers.Meta):
        fields = (
            'title',
            'description',
            'file',
            'semester',
        )


class ListAssignmentSerializers(AssignmentSerializers):
    user = serializers.CharField()
    date_created = serializers.DateTimeField(format=settings.DATE_TIME_FIELD_FORMAT)
    submission_date = serializers.DateTimeField(format=settings.DATE_TIME_FIELD_FORMAT)

    class Meta(AssignmentSerializers.Meta):
        fields = (
            'id',
            'title',
            'description',
            'file',
            'date_created',
            'user',
            'semester',
            'submission_date'
        )


class UpdateAssignmentSerializers(AssignmentSerializers):
    class Meta(AssignmentSerializers.Meta):
        fields = (
            'title',
            'description',
            'file',
            'semester',
        )
