from rest_framework import serializers

from apps.notice.models import Notice


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
        )


class ListNoticeSerializers(NoticeSerializers):
    class Meta(NoticeSerializers.Meta):
        fields = (
            'id',
            'title',
            'description',
            'image',
        )
