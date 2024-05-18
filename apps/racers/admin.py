from django.contrib import admin
from .models import Racer


class RacerAdmin(admin.ModelAdmin):
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(Racer, RacerAdmin)
