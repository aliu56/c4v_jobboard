# Generated by Django 3.2 on 2021-06-04 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0005_auto_20210604_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startup',
            old_name='website_url',
            new_name='company_website_url',
        ),
        migrations.AddField(
            model_name='startup',
            name='logo',
            field=models.ImageField(default=0, max_length=200, upload_to=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='startup',
            name='scraping_source_url',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='startup',
            name='stage',
            field=models.CharField(choices=[('N', 'Not defined'), ('S', 'Seed'), ('A', 'Series A'), ('B', 'Series B'), ('C', 'Series C')], default='N', max_length=100),
        ),
    ]
