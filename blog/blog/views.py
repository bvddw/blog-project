from django.views.generic import TemplateView, ListView
from main_app.models import Article, Comment, Topic, UserTopic
from main_app.services import get_sorted_articles, get_sorted_topics
from django.core.paginator import Paginator, Page
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class MainPage(ListView):
    paginate_by = 2
    template_name = 'index.html'
    context_object_name = 'sorted_articles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return get_sorted_articles(self.request.user.id)
        else:
            return Article.objects.all().order_by('-created_at')


# def main_page(request: HttpRequest) -> HttpResponse:
#     if request.user.is_authenticated:
#         articles = get_sorted_articles(request.user.id)
#     else:
#         articles = Article.objects.all().order_by('-created_at')
#     return render(request, 'index.html', {'sorted_articles': articles})


class AboutPage(TemplateView):
    template_name = "about.html"


# def archive(request: HttpRequest, year: str, month: str) -> HttpResponse:
#     months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#               'November', 'December']
#     return HttpResponse(f'Archive. Year: {year}, month: {months[int(month) - 1]}.')