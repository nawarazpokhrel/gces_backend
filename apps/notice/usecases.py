from datetime import datetime

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound
from apps.notice.models import Notice


class AddNoticeUseCase:
    def __init__(self, serializer, user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._user = user

    def execute(self):
        self._factory()

    def _factory(self):
        self._notice = Notice(**self._data, user=self._user)
        self._notice.save()


class ListNoticeUseCase:
    def execute(self):
        self._factory()
        return self._notice

    def _factory(self):
        self._notice = Notice.objects.all().order_by('-id')[:5]


class NoticeNotFound(NotFound):
    default_detail = _('Notice  Not found for following id')


class GetNoticeUseCase:
    def __init__(self, notice_id):
        self._notice_id = notice_id

    def execute(self):
        self._factory()
        return self.notice

    def _factory(self):
        try:
            self.notice = Notice.objects.get(pk=self._notice_id)
        except Notice.DoesNotExist:
            raise NoticeNotFound


# class UpdateNoticeUseCase:
class UpdateNoticeUseCase:
    def __init__(self, serializer, notice: Notice):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._notice = notice

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            # self._data.get(key)
            setattr(self._notice, key, self._data.get(key))
        self._notice.updated_date = datetime.now()
        self._notice.save()


class DeleteNoticeUseCase:
    def __init__(self,notice:Notice):
        self._notice = notice

    def execute(self):
        self._factory()

    def _factory(self):
        self._notice.delete()
