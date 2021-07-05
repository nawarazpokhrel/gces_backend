from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from apps.core.models import BaseModel
from apps.notice import validators
from apps.notice.utils import upload_notice_image_to
from django.db.models.signals import post_delete

from apps.core.utils import file_cleanup

User = get_user_model()


class Notice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_notice_image_to, validators=[validators.notice_image_validator])

    def __str__(self):
        return self.title


post_delete.connect(file_cleanup, sender=Notice, dispatch_uid="notice.file_cleanup")
