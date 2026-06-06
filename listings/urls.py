from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.house_list, name='house_list'),
    path('house/<int:pk>/', views.house_detail, name='house_detail'),
    
    # Routes d'authentification des locataires
    path('login/', auth_views.LoginView.as_view(template_name='listings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Nouvelle route de déconnexion propre
    
    path('register/', views.register, name='register'),
]