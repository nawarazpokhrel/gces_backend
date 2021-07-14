class ResponseMixin:
    response_serializer_class = None

    def get_response_serializer(self, *args, **kwargs):
        response_serializer_class = self.get_response_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return response_serializer_class(*args, **kwargs)

    def get_response_serializer_class(self):
        assert self.response_serializer_class is not None, (
            "'%s' should either include a `response_serializer_class` attribute, "
            "or override the `get_response_serializer()` method."
            % self.__class__.__name__
        )

        return self.response_serializer_class
