# Generated by Django 5.0.4 on 2024-05-14 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0004_alter_race_completion_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raceentry',
            old_name='position',
            new_name='place',
        ),
    ]
