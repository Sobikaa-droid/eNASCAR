from django.contrib import admin
from .models import Race, RaceEntry

admin.site.register([Race, RaceEntry])
