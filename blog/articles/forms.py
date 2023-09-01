from django import forms
from django.forms import ModelForm
from .models import Article, Comment
from topics.models import Topic


class CreateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topics']
        labels = {
            'title': 'Article Title',
            'content': 'Article Content',
            'topics': 'Topics',
            'author': 'Author',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "title",
                "placeholder": "Article Title",
                "name": "title"
            }),
            'content': forms.Textarea(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "content",
                "placeholder": "Article Content",
                "name": "content"
            }),
            'topics': forms.SelectMultiple(attrs={
                "class": "form-control shadow",
                "id": "topics",
                "name": "topics"
            }),
        }


class UpdateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topics']
        labels = {
            'title': 'Article Title',
            'content': 'Article Content',
            'topics': 'Topics',
            'author': 'Author',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "title",
                "placeholder": "Article Title",
                "name": "title"
            }),
            'content': forms.Textarea(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "content",
                "placeholder": "Article Content",
                "name": "content"
            }),
            'topics': forms.SelectMultiple(attrs={
                "class": "form-control shadow",
                "id": "topics",
                "name": "topics"
            }),
        }

    def update_article(self, article):
        article.title = self.cleaned_data['title']
        article.content = self.cleaned_data['content']
        article.topics.set(self.cleaned_data['topics'])
        article.save()
        return article.slug


class DeleteArticle(ModelForm):
    class Meta:
        model = Article
        fields = ['title']
        labels = {
            'title': 'Article Title'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "title",
                "placeholder": "Article Title",
                "name": "title",
            })
        }

    def delete_article(self, article):
        comments = Comment.objects.filter(article=article)
        article.delete()
        comments.delete()

    def clean(self):
        title = self.cleaned_data['title']
        real_title = self.initial.get('title')
        if real_title != title:
            self.add_error('title', 'Incorrect title.')


class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': 'Comment Message'
        }
        widgets = {
            'message': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control shadow",
                "id": "message",
                "placeholder": "Comment Message",
                "name": "message",
            })
        }
