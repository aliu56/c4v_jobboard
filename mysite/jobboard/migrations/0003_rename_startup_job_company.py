# Generated by Django 3.2 on 2021-06-03 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0002_auto_20210603_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='startup',
            new_name='company',
        ),
    ]
