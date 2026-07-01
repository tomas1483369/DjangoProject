from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('', views.dashboard, name='dashboard'),
]
