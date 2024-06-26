from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'races'

router = routers.DefaultRouter()
router.register(r'races', views.RaceAPIViewSet, basename="races")

urlpatterns = [
    # api
    path('api/', include(router.urls)),
    path('api/apply/<int:pk>/', views.ApplyForRaceAPIView.as_view(), name='api_apply_for_race'),
    path('api/cancel/<int:pk>/', views.CancelApplicationForRaceAPIView.as_view(), name='api_cancel_race'),
    path('api/complete-race/<int:pk>/', views.CompleteRaceAPIView.as_view(), name='api_complete_race'),
    path('api/race-entry/<int:race_pk>/', views.RaceEntryAPIListView.as_view(), name='api_race_entry_list'),
    path('api/race-entry/<int:race_pk>/racer/<int:racer_pk>/', views.RaceEntryAPIRetrieveView.as_view(), name='api_race_entry_detail'),
    # generic
    path('', views.RaceListView.as_view(), name='race_list'),
    path('completed/', views.CompletedRaceListView.as_view(), name='completed_race_list'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('<int:pk>/racers/', views.RaceEntryOfRaceListView.as_view(), name='race_racers_list'),
    path('apply/<int:pk>/', login_required(views.apply_for_race, login_url='api-auth'), name='apply_for_race'),
    path('cancel/<int:pk>/', login_required(views.cancel_application_for_race, login_url='api-auth'), name='cancel_race'),
]
