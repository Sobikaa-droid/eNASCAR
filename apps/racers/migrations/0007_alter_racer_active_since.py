# Generated by Django 5.0.4 on 2024-05-12 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racers', '0006_racer_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racer',
            name='active_since',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
