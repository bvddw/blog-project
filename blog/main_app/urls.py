"""
URL configuration for posts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('profile/<username>/', views.ProfileView.as_view(), name='profile_page'),
    path('set-password/<username>/', views.SetNewPasswordView.as_view(), name='set_password'),
    path('password_changed/', views.PasswordChanged.as_view(), name='password_changed'),
    path('set-userdata/<username>/', views.SetUserDataView.as_view(), name='set_data'),
    path('deactivate/', views.DeactivateAccountView.as_view(), name='deactivate'),
    path('reactivate/', views.ReactivateAccountView.as_view(), name='reactivate'),
    path('success_reactivation/', views.SuccessReactivationView.as_view(), name='success_reactivation'),
    path('login_user/', views.LoginUserView.as_view(), name='login_user'),
    path('register_user/', views.RegisterUserView.as_view(), name='register_user'),
    path('logout_user/', views.LogoutUserView.as_view(), name='logout_user'),
]
