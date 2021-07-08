from apps.notice import usecases


class NoticeMixin:
    def get_notice(self):
        return usecases.GetNoticeUseCase(
            notice_id=self.kwargs.get('notice_id')
        ).execute()
