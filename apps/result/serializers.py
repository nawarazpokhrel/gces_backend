from rest_framework import serializers

from apps.result.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class AddSubjectSerializer(ResultSerializer):
    class Meta(ResultSerializer.Meta):
        fields = (
            'gpa',
            'subject'
        )


class SubjectSerializer(ResultSerializer):

    class Meta(ResultSerializer.Meta):
        fields = (
            'gpa',
            'subject',
        )


class AddResultSerializer(ResultSerializer):
    subject = AddSubjectSerializer(many=True)

    class Meta(ResultSerializer.Meta):
        fields = (
            'semester',
            'subject',
        )


class ListResultSerializer(ResultSerializer):
    subject = SubjectSerializer(many=True, read_only=True)

    class Meta(ResultSerializer.Meta):
        fields = (
            'user',
            # 'gpa',
            'subject',
        )


class ResponseSerializer(serializers.Serializer):
    user = serializers.CharField()

