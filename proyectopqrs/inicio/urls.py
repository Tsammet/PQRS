from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', views.inicioC, name='inicioC'),
    path('interno/', login_required(views.inicioA), name='inicioA'),
]
