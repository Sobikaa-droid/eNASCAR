# Generated by Django 5.0.4 on 2024-05-08 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racers', '0005_alter_racer_number_alter_racer_year_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='racer',
            name='country',
            field=models.CharField(default='Prussia', max_length=70),
            preserve_default=False,
        ),
    ]
