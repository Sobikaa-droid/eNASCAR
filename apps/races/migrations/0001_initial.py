# Generated by Django 5.0.6 on 2024-05-19 01:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=1500, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('race_limit', models.IntegerField(default=10, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(2)])),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='RaceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, null=True)),
                ('place', models.IntegerField(blank=True, null=True)),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.race')),
                ('racer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='racers',
            field=models.ManyToManyField(blank=True, through='races.RaceEntry', to=settings.AUTH_USER_MODEL),
        ),
    ]
