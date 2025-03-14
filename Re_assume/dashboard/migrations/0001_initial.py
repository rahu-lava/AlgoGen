# Generated by Django 5.1.2 on 2025-03-09 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('credentials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.TextField()),
                ('experience', models.PositiveIntegerField()),
                ('position', models.CharField(max_length=255)),
                ('keywords', models.TextField(help_text='Enter keywords separated by commas')),
                ('english_level', models.IntegerField(default='')),
                ('current_rating', models.CharField(blank=True, max_length=5, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='credentials.user_table')),
            ],
        ),
    ]
