from django.db import models

# Create your models here.
from apps.core.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Result(BaseModel):
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
    registration_number = models.CharField(null=True,blank=True,max_length=20)
    semester = models.CharField(max_length=50,choices=semester_choices,null=True,blank=True)
    gpa = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    # title = models.CharField()

    def __str__(self):
        return '{} - of {}'.format(self.subject, self.user.fullname)
