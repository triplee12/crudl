# Generated by Django 4.0.5 on 2022-07-12 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avart',
            new_name='avatar',
        ),
    ]