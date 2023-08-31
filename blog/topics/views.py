from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from articles.models import Article
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from .models import Topic, UserTopic

UserModel = get_user_model()


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'one_topic.html'
    context_object_name = 'topic'

    def get_object(self, queryset=None):
        topic_title = self.kwargs.get('topic_title')
        return get_object_or_404(Topic, title=topic_title)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        topic = self.object
        articles = Article.objects.filter(topics=topic)
        context_data['articles'] = articles
        return context_data


class SubscribeTopicConfirmationView(View):
    template_name = 'sub_topic.html'
    model = Topic

    def get(self, request, topic_title):
        try:
            cur_topic = get_object_or_404(self.model, title=topic_title)
            ctx = {'topic': cur_topic}
            return render(request, self.template_name, ctx)
        except self.model.DoesNotExist:
            raise Http404('No topics with such title.')


class TopicPreferView(View):
    model = UserTopic

    def get(self, request, topic_title):
        topic = get_object_or_404(Topic, title=topic_title)

        try:
            rel = self.model.objects.get(user=request.user, topic=topic)
        except self.model.DoesNotExist:
            self.model.objects.create(user=request.user, topic=topic, notify=False)

        url = reverse('user:profile_page', kwargs={'username': request.user.username})
        return HttpResponseRedirect(url)


class TopicSubscribeView(View):
    model = UserTopic

    def get(self, request, topic_title):
        topic = get_object_or_404(Topic, title=topic_title)

        try:
            rel = self.model.objects.get(user=self.request.user, topic=topic)
            rel.notify = True
            rel.save()
        except self.model.DoesNotExist:
            self.model.objects.create(user=self.request.user, topic=topic, notify=True)

        url = reverse('user:profile_page', kwargs={'username': self.request.user.username})
        return HttpResponseRedirect(url)


class UnsubscribeTopicConfirmationView(View):
    template_name = 'unsub_topic.html'
    model = Topic

    def get(self, request, topic_title):
        try:
            cur_topic = get_object_or_404(self.model, title=topic_title)
            ctx = {'topic': cur_topic}
            return render(request, self.template_name, ctx)
        except self.model.DoesNotExist:
            raise Http404('No topics with such title.')


class TopicUnpreferView(View):
    model = UserTopic

    def get(self, request, topic_title):
        topic = get_object_or_404(Topic, title=topic_title)

        rel = self.model.objects.get(user=request.user, topic=topic)
        rel.delete()
        url = reverse('user:profile_page', kwargs={'username': request.user.username})
        return HttpResponseRedirect(url)


class TopicUnsubscribeView(View):
    model = UserTopic

    def get(self, request, topic_title):
        topic = get_object_or_404(Topic, title=topic_title)

        rel = self.model.objects.get(user=request.user, topic=topic)
        rel.notify = False
        rel.save()
        url = reverse('user:profile_page', kwargs={'username': request.user.username})
        return HttpResponseRedirect(url)