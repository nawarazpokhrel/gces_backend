from django.contrib import admin

# Register your models here.
from apps.result.models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )