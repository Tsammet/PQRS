from django.urls import path
from . import views



urlpatterns = [
    path('interno/', views.Login, name='entrar'),
    path('', views.log_out, name='log_out'),
  
]
