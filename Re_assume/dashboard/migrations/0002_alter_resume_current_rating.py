# Generated by Django 5.1.2 on 2025-03-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='current_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
