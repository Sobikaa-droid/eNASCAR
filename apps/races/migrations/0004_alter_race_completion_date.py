# Generated by Django 5.0.4 on 2024-05-10 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0003_alter_raceentry_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
