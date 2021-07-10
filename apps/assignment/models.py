from django.db import models
from datetime import datetime

from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
# Create your models here.
from apps.assignment.utils import upload_assignment_to
from apps.assignment.validators import validate_assignment
from apps.core.models import BaseModel

User = get_user_model()


class Assignment(BaseModel):
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
    file = models.FileField(upload_to=upload_assignment_to,
                            validators=[validate_assignment],
                            null=True,
                            blank=True)
    submission_date = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return '{} for {} semester to be submitted till {}'.format(
            self.title, self.semester, self.submission_date.date()
        )

    def save(self, *args, **kwargs):
        date_time = datetime.now()
        one_month_from_now = date_time + relativedelta(months=1)
        if self._state.adding:
            self.submission_date = one_month_from_now
        super(Assignment, self).save(*args, **kwargs)
