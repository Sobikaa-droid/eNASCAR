# Generated by Django 5.0.3 on 2024-04-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
