# Generated by Django 3.2.4 on 2021-06-30 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_joined_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='joined_date',
            new_name='batch',
        ),
    ]