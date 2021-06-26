from django.db import models

# Create your models here.
from shortuuidfield import ShortUUIDField


class BaseModel(models.Model):
    id = ShortUUIDField(
        primary_key=True,
        auto=True,
        editable=False,
        unique=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This model will  not be used to create any database table.
        abstract = True
