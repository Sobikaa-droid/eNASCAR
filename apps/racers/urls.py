from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

app_name = 'racers'

router = routers.DefaultRouter()
router.register(r'racers', views.RacerAPIViewSet, basename="racers")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.RacerListView.as_view(), name='racer_list'),
    path('<int:pk>/', views.RacerDetailView.as_view(), name='racer_detail'),
    path('update/<int:pk>/', login_required(views.RacerUpdateView.as_view(), login_url='api-auth'), name='racer_update'),
    path('register/', views.RacerRegisterView.as_view(), name='register'),
    path('login/', views.RacerLoginView.as_view(), name='login'),
    path('logout/', login_required(views.LogoutView.as_view(), login_url='api-auth'), name='logout'),
]
