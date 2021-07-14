from django.contrib.auth import get_user_model

from apps.result.models import Result

User = get_user_model()


class AddResultUseCase:
    def __init__(self, serializer, user: User, ):
        self._serializer = serializer
        self._user = user
        self._data = serializer.validated_data

    def execute(self):
        self._factory()
        # return self.res

    def _factory(self):
        # print(self._data)
        results = []
        print(self._data)
        subject = self._data.pop('subject')


        for data in subject:
            self.result = Result(user=self._user, **data)
            self.result.semester = self._data['semester']
            results.append(self.result)
        # self.result.user = self._user
        # print(self.result)
        # results.append(self.result.user)

        Result.objects.bulk_create(results)




class ListResultUseCase:
    def __init__(self, user: User):
        self._user = user

    def execute(self):
        self._factory()
        return self._result

    def _factory(self):
        self._result = Result.objects.filter(user=self._user)
        print(self._result)
