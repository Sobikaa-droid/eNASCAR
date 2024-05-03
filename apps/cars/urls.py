from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'cars'

urlpatterns = [
    path('api/', views.CarAPICreateView.as_view()),
    path('api/<int:pk>/', views.CarAPIRetrieveUpdateView.as_view()),
    path('create/', login_required(views.CarCreateView.as_view(), login_url='racers:register'), name='car_create'),
    path('update/<int:pk>/', login_required(views.CarUpdateView.as_view(), login_url='racers:register'), name='car_update'),
]