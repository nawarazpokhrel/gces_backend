# Generated by Django 3.2.5 on 2021-07-09 17:39

import apps.materials.utils
import apps.materials.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('semester', models.CharField(choices=[('first', 'First'), ('second', 'Second'), ('third', 'Third'), ('fourth', 'Fourth'), ('fifth', 'Fifth'), ('sixth', 'Sixth'), ('seventh', 'Seventh'), ('eight', 'Eight'), ('all', 'All')], max_length=256)),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.materials.utils.upload_materials_to, validators=[apps.materials.validators.MaterialValidator()])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
