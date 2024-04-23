from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'racers'

urlpatterns = [
    path('', views.RacerListView.as_view(), name='racer_list'),
    path('<int:pk>/', views.RacerDetailView.as_view(), name='racer_detail'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
