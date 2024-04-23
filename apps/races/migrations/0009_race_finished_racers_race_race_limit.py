# Generated by Django 5.0.4 on 2024-04-17 22:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0008_alter_race_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='finished_racers',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='race',
            name='race_limit',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(2)]),
        ),
    ]
