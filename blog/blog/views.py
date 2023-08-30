from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, ListView
from articles.models import Article
from main_app.services import get_sorted_articles

UserModel = get_user_model()


class MainPage(ListView):
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'sorted_articles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return get_sorted_articles(self.request.user.id)
        else:
            return Article.objects.all().order_by('-created_at')


class AboutPage(TemplateView):
    template_name = "about.html"
