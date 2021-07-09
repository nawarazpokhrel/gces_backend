from rest_framework import serializers

from apps.materials.models import Material
from gces_backend import settings


class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class AddNoticeSerializers(MaterialSerializers):
    class Meta(MaterialSerializers.Meta):
        fields = (
            'title',
            'description',
            'file',
            'semester',
        )


class ListMaterialSerializers(MaterialSerializers):
    user = serializers.CharField()
    date_created = serializers.DateTimeField(format=settings.DATE_TIME_FIELD_FORMAT)

    class Meta(MaterialSerializers.Meta):
        fields = (
            'id',
            'title',
            'description',
            'file',
            'date_created',
            'user',
            'semester',
        )


class UpdateMaterialsSerializers(MaterialSerializers):
    class Meta(MaterialSerializers.Meta):
        fields = (
            'title',
            'description',
            'file',
            'semester',
        )
