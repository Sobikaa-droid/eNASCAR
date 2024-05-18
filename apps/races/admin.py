from django.contrib import admin
from .models import Race, RaceEntry


class RaceAdmin(admin.ModelAdmin):
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(Race, RaceAdmin)


class RaceEntryAdmin(admin.ModelAdmin):
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related('race', 'racer')
        return qs


admin.site.register(RaceEntry, RaceEntryAdmin)
