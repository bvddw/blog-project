from .email_settings import email_password
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from articles.models import Article, Comment
from email.message import EmailMessage
import ssl
import smtplib

UserModel = get_user_model()


class LoginUser(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control shadow",
            "id": "username",
            "placeholder": "Username",
            "name": "username"
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "password",
            "placeholder": "Password",
            "name": "password"
        }
    ))

    def clean(self):
        if not authenticate(**self.cleaned_data):
            raise ValidationError("Incorrect username or password.")


class RegistrateUser(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control shadow",
            "id": "username",
            "placeholder": "Username",
            "name": "username"
        }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            "type": "email",
            "class": "form-control shadow",
            "id": "email",
            "placeholder": "Email",
            "name": "email"
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "password",
            "placeholder": "Password",
            "name": "password"
        }
    ))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "confirmPassword",
            "placeholder": "Confirm Password",
            "name": "confirm_password"
        }
    ))

    def create_user(self):
        del self.cleaned_data["confirm_password"]
        UserModel.objects.create_user(**self.cleaned_data)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserModel.objects.get(username=username)
            raise ValidationError("User with this username already registered.")
        except UserModel.DoesNotExist:
            return username

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            self.add_error("password", "Does not match")
            self.add_error("confirm_password", "Does not match")


class SetUserData(forms.Form):
    first_name = forms.CharField(label="First name", required=False, widget=forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control shadow",
            "id": "first name",
            "placeholder": "First name",
            "name": "first_name",
        }
    ))
    last_name = forms.CharField(label="Last name", required=False, widget=forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control shadow",
            "id": "last name",
            "placeholder": "Last name",
            "name": "last_name"
        }
    ))
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            "type": "email",
            "class": "form-control shadow",
            "id": "email",
            "placeholder": "Email",
            "name": "email"
        }
    ))

    def update_data(self, username):
        user = UserModel.objects.get(username=username)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()


class SetNewPassword(forms.Form):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "oldPassword",
            "placeholder": "Old password",
            "name": "old_password"
        }
    ))
    new_password = forms.CharField(label="New password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "newPassword",
            "placeholder": "New password",
            "name": "new_password"
        }
    ))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control shadow",
            "id": "confirmPassword",
            "placeholder": "Confirm Password",
            "name": "confirm_password"
        }
    ))

    def update_data(self, username):
        user = UserModel.objects.get(username=username)
        new_password = self.cleaned_data["new_password"]
        user.set_password(new_password)
        user.save()

    def clean(self):
        old_password = self.cleaned_data["old_password"]
        username = self.initial.get("username")  # Assume you pass the username when initializing the form
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise forms.ValidationError("User does not exist")

        if not user.check_password(old_password):
            self.add_error("old_password", "Incorrect old password")
        new_password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if new_password != confirm_password:
            self.add_error("new_password", "Does not match")
            self.add_error("confirm_password", "Does not match")


class Reactivate(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            "type": "Email",
            "class": "form-control shadow",
            "id": "Email",
            "placeholder": "Email",
            "name": "email"
        }
    ))

    def reactivate(self):
        user = UserModel.objects.get(email=self.cleaned_data["email"])
        user.is_active = True
        user.set_password('reactivated_pass')
        user.save()

        email_sender = 'post.blog239@gmail.com'
        email_receiver = user.email
        subject = 'Account reactivation'
        body = """
Your account was reactivate successfully! We changed your password to: "reactivated_pass", please change it on your own after log in.

Sincerely, Team PostBlog!"""
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def clean(self):
        email = self.cleaned_data["email"]
        if email not in UserModel.objects.all().values_list('email', flat=True):
            self.add_error("email", "No registered users with this email.")
        elif UserModel.objects.get(email=email).is_active:
            self.add_error("email", "Account with this email is active.")


# class CreateArticle(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'content', 'topics']
#         labels = {
#             'title': 'Article Title',
#             'content': 'Article Content',
#             'topics': 'Topics',
#             'author': 'Author',
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "title",
#                 "placeholder": "Article Title",
#                 "name": "title"
#             }),
#             'content': forms.Textarea(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "content",
#                 "placeholder": "Article Content",
#                 "name": "content"
#             }),
#             'topics': forms.SelectMultiple(attrs={
#                 "class": "form-control shadow",
#                 "id": "topics",
#                 "name": "topics"
#             }),
#         }
#
#
# class UpdateArticle(ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'content', 'topics']
#         labels = {
#             'title': 'Article Title',
#             'content': 'Article Content',
#             'topics': 'Topics',
#             'author': 'Author',
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "title",
#                 "placeholder": "Article Title",
#                 "name": "title"
#             }),
#             'content': forms.Textarea(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "content",
#                 "placeholder": "Article Content",
#                 "name": "content"
#             }),
#             'topics': forms.SelectMultiple(attrs={
#                 "class": "form-control shadow",
#                 "id": "topics",
#                 "name": "topics"
#             }),
#         }
#
#     def update_article(self, article):
#         article.title = self.cleaned_data['title']
#         article.content = self.cleaned_data['content']
#         article.topics.set(self.cleaned_data['topics'])
#         article.save()
#         return article.slug
#
#
# class DeleteArticle(ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title']
#         labels = {
#             'title': 'Article Title'
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "title",
#                 "placeholder": "Article Title",
#                 "name": "title",
#             })
#         }
#
#     def delete_article(self, article):
#         comments = Comment.objects.filter(article=article)
#         article.delete()
#         comments.delete()
#
#     def clean(self):
#         title = self.cleaned_data['title']
#         real_title = self.initial.get('title')
#         if real_title != title:
#             self.add_error('title', 'Incorrect title.')
#
#
# class CreateComment(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['message']
#         labels = {
#             'message': 'Comment Message'
#         }
#         widgets = {
#             'message': forms.TextInput(attrs={
#                 "type": "text",
#                 "class": "form-control shadow",
#                 "id": "message",
#                 "placeholder": "Comment Message",
#                 "name": "message",
#             })
#         }
