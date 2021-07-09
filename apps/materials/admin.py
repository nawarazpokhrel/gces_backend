from django.contrib import admin

# Register your models here.
from apps.materials.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'date_created'
    )

    list_display_links = (
        'id',
        'user',
    )
