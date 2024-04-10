"""
URL configuration for nascar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers

from apps.races.views import RaceAPIViewSet
from apps.racers.views import RacerAPIViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'races', RaceAPIViewSet, basename="races")
router.register(r'racers', RacerAPIViewSet, basename="racers")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # for DRF auth
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('racers/', include(('apps.racers.urls', 'racers'))),
    path('races/', include(('apps.races.urls', 'races'))),
]
