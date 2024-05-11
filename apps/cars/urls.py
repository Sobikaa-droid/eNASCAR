from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'cars'

router = routers.DefaultRouter()
router.register(r'car_models', views.CarModelAPIViewSet, basename="car_models")

urlpatterns = [
    # api
    path('api/', include(router.urls)),
    path('api/cars/', views.CarAPICreateView.as_view()),
    path('api/cars/<int:pk>/', views.CarAPIRetrieveUpdateDeleteView.as_view()),
    # generic
    path('create/', login_required(views.CarCreateView.as_view(), login_url='racers:register'), name='car_create'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('update/<int:pk>/', login_required(views.CarUpdateView.as_view(), login_url='racers:register'), name='car_update'),
    path('delete/<int:pk>/', login_required(views.CarDeleteView.as_view(), login_url='racers:register'), name='car_delete'),
]