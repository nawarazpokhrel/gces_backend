from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
from apps.core.models import BaseModel
from apps.materials.utils import upload_materials_to
from apps.materials.validators import validate_material

User = get_user_model()


class Material(BaseModel):
    semester_choices = (
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('fourth', 'Fourth'),
        ('fifth', 'Fifth'),
        ('sixth', 'Sixth'),
        ('seventh', 'Seventh'),
        ('eight', 'Eight'),
        ('all', 'All'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    semester = models.CharField(max_length=256, choices=semester_choices)
    file = models.FileField(upload_to=upload_materials_to,
                            validators=[validate_material],
                            null=True,
                            blank=True)

    def __str__(self):
        return '{} for {}'.format(self.title, self.semester)
