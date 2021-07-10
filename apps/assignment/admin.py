from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from apps.assignment.models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'date_created',
    )

    list_display_links = (
        'id',
        'user',
        'title',
    )
    readonly_fields = (
        'submission_date',
    )
