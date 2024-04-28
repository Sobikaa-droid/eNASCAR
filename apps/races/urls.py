from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'races'

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('<int:pk>/racers/', views.RaceRacersListView.as_view(), name='race_racers_list'),
    path('apply/<int:pk>/', login_required(views.apply_for_race, login_url='api-auth'), name='apply_for_race'),
    path('cancel_race/<int:pk>/', login_required(views.cancel_application_for_race, login_url='api-auth'), name='cancel_race'),
]
