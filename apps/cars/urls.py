from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'cars'

router = routers.DefaultRouter()
router.register(r'car_models', views.CarModelAPIViewSet, basename="car_models")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/cars/', views.CarAPICreateView.as_view()),
    path('api/cars/<int:pk>/', views.CarAPIRetrieveUpdateView.as_view()),
    path('create/', login_required(views.CarCreateView.as_view(), login_url='racers:register'), name='car_create'),
    path('update/<int:pk>/', login_required(views.CarUpdateView.as_view(), login_url='racers:register'), name='car_update'),
]