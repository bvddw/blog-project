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
    path('create/', views.CreateArticleView.as_view(), name='create_article'),
    path('no-access/', views.NoAccess.as_view(), name='no_access'),
    path('<slug:article_slug>/', views.ArticleView.as_view(), name='one_article'),
    path('<slug:article_slug>/update/', views.UpdateArticleView.as_view(), name='upd_article'),
    path('<slug:article_slug>/delete/', views.DeleteArticleView.as_view(), name='del_article'),
]