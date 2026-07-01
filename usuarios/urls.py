from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
