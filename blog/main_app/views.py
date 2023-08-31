from articles.models import Article
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from main_app.forms import LoginUser, RegistrateUser, SetUserData, SetNewPassword, Reactivate
from main_app.services import get_sorted_articles, get_sorted_topics
from .models import UserModel


class ProfileView(DetailView):
    model = UserModel
    template_name = 'user_profile_page.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        cur_user = self.get_object()
        articles = Article.objects.filter(author=cur_user)
        articles_on_preferred_topics = get_sorted_articles(cur_user.id)[:3]
        sorted_topics = get_sorted_topics(cur_user)
        context_data['users_articles'] = articles
        context_data['recommendation'] = articles_on_preferred_topics
        context_data['ordered_topics'] = sorted_topics
        return context_data


class SetNewPasswordView(View):
    template_name = 'set_password.html'
    model = UserModel
    form_class = SetNewPassword

    def get(self, request, username):
        user = get_object_or_404(self.model, username=username)
        if not request.user.is_authenticated:
            url = reverse('login_user')
            return HttpResponseRedirect(url)
        form = self.form_class(initial={'username': username})
        return render(request, self.template_name, {'form': form})

    def post(self, request, username):
        form = SetNewPassword(request.POST, initial={'username': username})
        if form.is_valid():
            form.update_data(username)

            url = reverse('user:password_changed')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class PasswordChanged(View):
    template_name = 'password_changed.html'

    def get(self, reqeust):
        return render(reqeust, self.template_name)


def set_userdata(request: HttpRequest, username) -> HttpResponse:
    try:
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        raise Http404
    if not request.user.is_authenticated:
        url = reverse('login_user')
        return HttpResponseRedirect(url)
    if request.method == "POST":
        form = SetUserData(request.POST)
        if form.is_valid():
            form.update_data(username)

            url = reverse('user:profile_page', kwargs={'username': username})
            return HttpResponseRedirect(url)
    else:
        fields = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        form = SetUserData(fields)
    return render(request, 'set_data.html', {"form": form})


class SetUserDataView(View):
    template_name = 'set_data.html'
    model = UserModel
    form_class = SetUserData

    def get(self, request, username):
        user = get_object_or_404(self.model, username=username)
        if not request.user.is_authenticated:
            url = reverse('login_user')
            return HttpResponseRedirect(url)
        details = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        form = SetUserData(details)
        return render(request, self.template_name, {'form': form})

    def post(self, request, username):
        form = SetUserData(request.POST)
        if form.is_valid():
            form.update_data(username)

            url = reverse('user:profile_page', kwargs={'username': username})
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class DeactivateAccountView(View):
    template_name = 'deactivate.html'

    def get(self, request):
        if not request.user.is_authenticated:
            url = reverse('user:login_user')
            return HttpResponseRedirect(url)
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        logout(request)
        user.is_active = False
        user.save()
        url = reverse('user:login_user')
        return HttpResponseRedirect(url)


class ReactivateAccountView(View):
    template_name = 'reactivate.html'
    form_class = Reactivate

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.reactivate()

            url = reverse('user:success_reactivation')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class SuccessReactivationView(View):
    template_name = 'success_reactivation.html'

    def get(self, reqeust):
        return render(reqeust, self.template_name)


class LoginUserView(View):
    template_name = 'login.html'
    form_class = LoginUser

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            login(request, user)

            url = reverse('user:profile_page', kwargs={'username': user.username})
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class RegisterUserView(View):
    template_name = 'register.html'
    form_class = RegistrateUser

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.create_user()

            url = reverse('user:login_user')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        url = reverse('main_page')
        return HttpResponseRedirect(url)