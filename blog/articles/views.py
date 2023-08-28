from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from main_app.models import Article, Comment, Topic
from main_app.forms import CreateArticle, CreateComment, UpdateArticle, DeleteArticle
from django.urls import reverse


def article(request: HttpRequest, article_slug) -> HttpResponse:
    # display only article content, comments on page /article_title/comments
    try:
        user = request.user
        cur_article = Article.objects.get(slug=article_slug)

        if request.method == "POST":
            form = CreateComment(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']

                new_comment = Comment.objects.create(message=message, author=user, article=cur_article)
        else:
            form = CreateComment()
        ctx = {
            'article': cur_article,
            'comments': Comment.objects.filter(article=Article.objects.get(slug=article_slug)),
            'form': form,
        }
        return render(request, 'one_article.html', ctx)
    except Article.DoesNotExist:
        raise Http404('There no such article.')


def update_article(request: HttpRequest, article_slug) -> HttpResponse:
    try:
        cur_article = Article.objects.get(slug=article_slug)
        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)
        if request.method == 'POST':
            form = UpdateArticle(request.POST)
            if form.is_valid():
                new_slug = form.update_article(cur_article)

                url = reverse('articles:one_article', kwargs={'article_slug': new_slug})
                return HttpResponseRedirect(url)  # Redirect to a view displaying the list of articles
        else:
            fields = {"title": cur_article.title, "content": cur_article.content, "topics": cur_article.topics}
            form = UpdateArticle(fields)
        return render(request, 'upd_article.html', {'form': form, 'slug': article_slug})
    except Article.DoesNotExist:
        raise Http404('No articles with such title.')


def delete_article(request: HttpRequest, article_slug) -> HttpResponse:
    try:
        cur_article = Article.objects.get(slug=article_slug)
        if request.user != cur_article.author:
            url = reverse('articles:no_access')
            return HttpResponseRedirect(url)
        if request.method == "POST":
            form = DeleteArticle(request.POST, initial={'title': cur_article.title})
            if form.is_valid():
                form.delete_article(cur_article)

                url = reverse('main_page')
                return HttpResponseRedirect(url)
        else:
            form = DeleteArticle()
        return render(request, 'del_article.html', {'form': form, 'slug': article_slug})
    except Article.DoesNotExist:
        raise Http404('No articles with such title.')


def create_article(request):
    if not request.user.username:
        url = reverse('user:login_user')
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        form = CreateArticle(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topics = form.cleaned_data['topics']

            # Assuming Article model has a ManyToMany relationship with Topic
            new_article = Article.objects.create(title=title, content=content, author=request.user)
            new_article.topics.set(topics)
            url = reverse('main_page')
            return HttpResponseRedirect(url)  # Redirect to a view displaying the list of articles
    else:
        form = CreateArticle()

    return render(request, 'create_article.html', {'form': form})


def no_access(request):
    return render(request, 'no_access.html')