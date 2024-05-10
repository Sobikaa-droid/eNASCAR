from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'races'

router = routers.DefaultRouter()
router.register(r'races', views.RaceAPIViewSet, basename="races")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.RaceListView.as_view(), name='race_list'),
    path('completed/', views.CompletedRaceListView.as_view(), name='completed_race_list'),
    path('api/complete_race/<int:pk>/', views.complete_race, name='complete_race'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('<int:pk>/racers/', views.RaceRacersListView.as_view(), name='race_racers_list'),
    path('apply/<int:pk>/', login_required(views.apply_for_race, login_url='api-auth'), name='apply_for_race'),
    path('cancel_race/<int:pk>/', login_required(views.cancel_application_for_race, login_url='api-auth'), name='cancel_race'),
]
