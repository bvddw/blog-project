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
    path('<topic_title>/', views.TopicDetailView.as_view(), name='one_topic'),
    path('<topic_title>/subscribe/', views.SubscribeTopicConfirmationView.as_view(), name='sub_topic'),
    path('<topic_title>/prefer/', views.TopicPreferView.as_view(), name='prefer_topic'),
    path('<topic_title>/subscribed/', views.TopicSubscribeView.as_view(), name='subd_topic'),
    path('<topic_title>/unsubscribe/', views.UnsubscribeTopicConfirmationView.as_view(), name='unsub_topic'),
    path('<topic_title>/unprefer/', views.TopicUnpreferView.as_view(), name='unprefer_topic'),
    path('<topic_title>/unsubscribed/', views.TopicUnsubscribeView.as_view(), name='unsubd_topic'),
]
