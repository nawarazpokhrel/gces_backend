from rest_framework import serializers

from apps.notice.models import Notice
from gces_backend import settings


class NoticeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class AddNoticeSerializers(NoticeSerializers):
    class Meta(NoticeSerializers.Meta):
        fields = (
            'title',
            'description',
            'image',
            'semester',
        )


class ListNoticeSerializers(NoticeSerializers):
    user = serializers.CharField()
    date_created = serializers.DateTimeField(format=settings.DATE_TIME_FIELD_FORMAT)

    class Meta(NoticeSerializers.Meta):
        fields = (
            'id',
            'title',
            'description',
            'image',
            'date_created',
            'user',
            'semester',
        )




class UpdateNoticeSerializers(NoticeSerializers):
    class Meta(NoticeSerializers.Meta):
        fields = (
            'title',
            'description',
            'image',
            'semester',
        )
