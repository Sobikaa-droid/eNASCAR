from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'races'

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
]
