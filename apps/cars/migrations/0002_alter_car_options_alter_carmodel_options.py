# Generated by Django 5.0.4 on 2024-05-06 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['-pk']},
        ),
    ]