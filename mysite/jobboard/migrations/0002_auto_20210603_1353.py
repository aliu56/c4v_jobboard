# Generated by Django 3.2 on 2021-06-03 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='offer_url',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='job',
            name='startup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobboard.startup'),
        ),
    ]
