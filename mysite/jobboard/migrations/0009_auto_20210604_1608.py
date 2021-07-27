# Generated by Django 3.2 on 2021-06-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0008_auto_20210604_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='city',
            field=models.CharField(max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='job',
            name='country',
            field=models.CharField(max_length=50, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_name',
            field=models.CharField(max_length=200, verbose_name='Job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='offer_url',
            field=models.CharField(max_length=500, verbose_name='Offer Link'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='company_website_url',
            field=models.CharField(max_length=200, verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='logo',
            field=models.ImageField(max_length=200, upload_to=None, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='scraping_source_url',
            field=models.CharField(max_length=200, verbose_name='Syncing source:'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='sector',
            field=models.CharField(choices=[('N', '-'), ('B2BO', 'B2B Services / Operation'), ('CONS', 'Consumer'), ('DATA', 'Data'), ('HEAL', 'Health'), ('INSU', 'InsurTech'), ('NEWI', 'New Infrastructure / Computing'), ('SAAS', 'SaaS'), ('TECH', 'Tech'), ('O', 'Other')], default='N', max_length=100, verbose_name='Sector'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='stage',
            field=models.CharField(choices=[('N', '-'), ('S', 'Seed'), ('A', 'Series A'), ('B', 'Series B'), ('C', 'Series C'), ('O', 'Other')], default='N', max_length=100, verbose_name='Stage'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='startup_name',
            field=models.CharField(max_length=200, verbose_name='Company'),
        ),
    ]