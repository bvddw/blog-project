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
    path('profile/<username>/', views.profile, name='profile_page'),
    path('set-password/<username>/', views.set_password, name='set_password'),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('set-userdata/<username>/', views.set_userdata, name='set_data'),
    path('deactivate/', views.deactivate, name='deactivate'),
    path('reactivate/', views.reactivate, name='reactivate'),
    path('success_reactivation/', views.success_reactivation, name='success_reactivation'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
]