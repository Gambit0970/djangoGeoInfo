from django.urls import path
from . import views


urlpatterns = [
    path('Meteo/', views.temp_here, name='temp_here'),
    path('Meteo/discover', views.temp_somewhere, name='temp_somewhere'),
]