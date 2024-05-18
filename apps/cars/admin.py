from django.contrib import admin
from .models import Car, CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(CarModel, CarModelAdmin)


class CarAdmin(admin.ModelAdmin):
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('car_model')
        return qs


admin.site.register(Car, CarAdmin)
