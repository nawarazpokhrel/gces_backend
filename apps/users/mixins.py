from apps.users.usecases import GetUserUseCase


class UserMixin:
    def get_user(self):
        return GetUserUseCase(
            user_id=self.kwargs.get('user_id')
        ).execute()
