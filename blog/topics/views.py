from django.http import HttpRequest, HttpResponse, Http404
from main_app.models import Article, Comment, Topic, UserTopic
from django.contrib.auth import get_user_model
from django.shortcuts import render

UserModel = get_user_model()


def one_topic(request: HttpRequest, topic_title: str):
    try:
        ctx = {
            'topic': Topic.objects.get(title=topic_title),
            'topics': Topic.objects.all(),
            'articles': Article.objects.filter(topics=Topic.objects.get(title=topic_title))
        }
        return render(request, 'one_topic.html', ctx)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')


def subscribe_topic(request: HttpRequest, topic_title) -> HttpResponse:
    try:
        cur_topic = Topic.objects.get(title=topic_title)
        ctx = {'topic': cur_topic}
        return render(request, 'sub_topic.html', ctx)
    except Topic.DoesNotExist:
        raise Http404('No topics with such title.')


def unsubscribe_topic(request: HttpRequest, topic_title) -> HttpResponse:
    try:
        cur_topic = Topic.objects.get(title=topic_title)
        ctx = {'topic': cur_topic}
        return render(request, 'unsub_topic.html', ctx)
    except Topic.DoesNotExist:
        raise Http404('No topics with such title.')
