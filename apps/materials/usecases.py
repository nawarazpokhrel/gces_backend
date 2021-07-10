from datetime import datetime

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from apps.materials.models import Material
from apps.notice.models import Notice


class AddMaterialUseCase:
    def __init__(self, serializer, user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._user = user

    def execute(self):
        self._factory()

    def _factory(self):
        self._material = Material(**self._data, user=self._user)
        self._material.save()


class ListMaterialUseCase:
    def execute(self):
        self._factory()
        return self._material

    def _factory(self):
        self._material = Material.objects.all()


class MaterialNotFound(NotFound):
    default_detail = _('Material  Not found for following id')


class GetMaterialUseCase:
    def __init__(self, material_id):
        self._material_id = material_id

    def execute(self):
        self._factory()
        return self.notice

    def _factory(self):
        try:
            self.notice = Material.objects.get(pk=self._material_id)
        except Material.DoesNotExist:
            raise MaterialNotFound


# class UpdateNoticeUseCase:
class UpdateMaterialUseCase:
    def __init__(self, serializer, material: Material):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._material = material

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            # self._data.get(key)
            setattr(self._material, key, self._data.get(key))
        self._material.updated_date = datetime.now()
        self._material.save()


class DeleteMaterialUseCase:
    def __init__(self, material: Material):
        self._material = material

    def execute(self):
        self._factory()

    def _factory(self):
        self._material.delete()
