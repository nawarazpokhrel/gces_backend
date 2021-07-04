from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class Validator:
    message = None
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        raise NotImplementedError("Subclasses should implement this!")

    def __eq__(self, other):
        return (
            isinstance(other, Validator) and
            (self.message == other.message) and
            (self.code == other.code)
        )


class ImageValidator(Validator):
    message = 'Image larger than 4 mb not allowed'
    file_size = 4194304

    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code)

        if value.size > self.file_size:
            raise ValidationError(self.message, code=self.code)
