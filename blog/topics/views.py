from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from articles.models import Article
from django.urls import reverse

from .models import Topic, UserTopic

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


def topic_prefer(request: HttpRequest, topic_title) -> HttpResponse:
    try:
        rel = UserTopic.objects.get(user=request.user, topic=get_object_or_404(Topic, title=topic_title))
    except UserTopic.DoesNotExist:
        UserTopic.objects.create(user=request.user, topic=get_object_or_404(Topic, title=topic_title), notify=False)
    url = reverse('user:profile_page', kwargs={'username': request.user.username})
    return HttpResponseRedirect(url)


def topic_subscribed(request: HttpRequest, topic_title) -> HttpResponse:
    try:
        rel = UserTopic.objects.get(user=request.user, topic=get_object_or_404(Topic, title=topic_title))
        rel.notify = True
        rel.save()
    except UserTopic.DoesNotExist:
        UserTopic.objects.create(user=request.user, topic=get_object_or_404(Topic, title=topic_title), notify=True)
    url = reverse('user:profile_page', kwargs={'username': request.user.username})
    return HttpResponseRedirect(url)


def unsubscribe_topic(request: HttpRequest, topic_title) -> HttpResponse:
    try:
        cur_topic = Topic.objects.get(title=topic_title)
        ctx = {'topic': cur_topic}
        return render(request, 'unsub_topic.html', ctx)
    except Topic.DoesNotExist:
        raise Http404('No topics with such title.')


def topic_unprefer(request: HttpRequest, topic_title) -> HttpResponse:
    rel = UserTopic.objects.get(user=request.user, topic=get_object_or_404(Topic, title=topic_title))
    rel.delete()
    url = reverse('user:profile_page', kwargs={'username': request.user.username})
    return HttpResponseRedirect(url)


def topic_unsubscribed(request: HttpRequest, topic_title) -> HttpResponse:
    rel = UserTopic.objects.get(user=request.user, topic=get_object_or_404(Topic, title=topic_title))
    rel.notify = False
    rel.save()
    url = reverse('user:profile_page', kwargs={'username': request.user.username})
    return HttpResponseRedirect(url)