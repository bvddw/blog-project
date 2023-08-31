from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from .models import Article, Comment
from .forms import CreateArticle, CreateComment, UpdateArticle, DeleteArticle
from django.urls import reverse
from django.views import View
from django.shortcuts import render, get_object_or_404


class ArticleView(View):
    template_name = 'article_details.html'
    comment_form_class = CreateComment

    def get(self, request, article_slug):
        try:
            cur_article = get_object_or_404(Article, slug=article_slug)
            comments = Comment.objects.filter(article=cur_article)
            form = self.comment_form_class()

            ctx = {
                'article': cur_article,
                'comments': comments,
                'form': form,
            }
            return render(request, self.template_name, ctx)
        except Article.DoesNotExist:
            raise Http404('There is no such article.')

    def post(self, request, article_slug):
        cur_article = get_object_or_404(Article, slug=article_slug)
        form = self.comment_form_class(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']
            new_comment = Comment.objects.create(message=message, author=request.user, article=cur_article)

        return HttpResponseRedirect(request.path)


class CreateArticleView(View):
    template_name = 'create_article.html'
    form_class = CreateArticle

    def get(self, request):
        if not request.user.username:
            url = reverse('user:login_user')
            return HttpResponseRedirect(url)

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topics = form.cleaned_data['topics']

            new_article = Article.objects.create(title=title, content=content, author=request.user)
            new_article.topics.set(topics)

            url = reverse('main_page')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class UpdateArticleView(View):
    template_name = 'upd_article.html'
    form_class = UpdateArticle

    def get(self, request, article_slug):
        cur_article = get_object_or_404(Article, slug=article_slug)

        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)

        details = {"title": cur_article.title, "content": cur_article.content, "topics": cur_article.topics.all()}
        form = self.form_class(initial=details, instance=cur_article)
        return render(request, self.template_name, {'form': form, 'slug': article_slug})

    def post(self, request, article_slug):
        cur_article = get_object_or_404(Article, slug=article_slug)

        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)

        form = self.form_class(request.POST)
        if form.is_valid():
            new_slug = form.update_article(cur_article)
            url = reverse('articles:one_article', kwargs={'article_slug': new_slug})
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form, 'slug': article_slug})


class DeleteArticleView(View):
    template_name = 'del_article.html'
    form_class = DeleteArticle

    def get(self, request, article_slug):
        cur_article = get_object_or_404(Article, slug=article_slug)

        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)

        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'slug': article_slug})

    def post(self, request, article_slug):
        cur_article = get_object_or_404(Article, slug=article_slug)

        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)

        form = self.form_class(request.POST, initial={'title': cur_article.title})
        if form.is_valid():
            form.delete_article(cur_article)
            url = reverse('main_page')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form, 'slug': article_slug})


class NoAccess(View):
    template_name = 'no_access.html'

    def get(self, request):
        return render(request, self.template_name)