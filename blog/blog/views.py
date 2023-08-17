from django.http import HttpRequest, HttpResponse
from main_app.models import Article, Comment, Topic, UserTopic
from main_app.services import get_sorted_articles, get_sorted_topics
from django.contrib.auth import get_user_model
from django.shortcuts import render

UserModel = get_user_model()


def main_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        articles = get_sorted_articles(request.user.id)
    else:
        articles = Article.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'sorted_articles': articles})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')


def archive(request: HttpRequest, year: str, month: str) -> HttpResponse:
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return HttpResponse(f'Archive. Year: {year}, month: {months[int(month) - 1]}.')