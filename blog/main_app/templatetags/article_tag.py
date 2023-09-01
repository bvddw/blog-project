from django import template
from articles.models import Article

register = template.Library()


@register.simple_tag(name='get_articles')
def custom_article_tag():
    return Article.objects.all()


@register.inclusion_tag('article_view.html')
def display_article(article):
    return {'article': article}
