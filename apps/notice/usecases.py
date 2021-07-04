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
