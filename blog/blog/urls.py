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
from django.contrib import admin
from django.urls import path, re_path, include
from .views import *

app_name = 'main_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main_page'),
    path('about/', AboutPage.as_view(), name='about_page'),
    # re_path(r'^archive\/(?P<year>\d{4})\/(?P<month>1[0-2]|0?[1-9])\/$', views.archive),
    path('', include(('main_app.urls', 'main_app'), namespace='user')),
    path('articles/', include(('articles.urls', 'articles'), namespace='articles')),
    path('topics/', include(('topics.urls', 'topics'), namespace='topics')),
]
