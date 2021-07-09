from apps.core.validators import FileValidator
from django.utils.translation import gettext_lazy as _


class MaterialValidator(FileValidator):
    message = _('The maximum size of file that uploaded is 5MB.')


validate_material = MaterialValidator()
