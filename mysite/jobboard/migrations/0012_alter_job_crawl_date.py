# Generated by Django 3.2 on 2021-06-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0011_auto_20210630_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='crawl_date',
            field=models.DateTimeField(verbose_name='Date of the crawl'),
        ),
    ]
