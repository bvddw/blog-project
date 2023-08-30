from articles.models import Article
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main_app.forms import LoginUser, RegistrateUser, SetUserData, SetNewPassword, Reactivate
from main_app.services import get_sorted_articles, get_sorted_topics
from topics.models import Topic

UserModel = get_user_model()


def profile(request: HttpRequest, username) -> HttpResponse:
    try:
        cur_user = UserModel.objects.get(username=username)
        articles = Article.objects.filter(author=cur_user)
        articles_on_preferred_topics = get_sorted_articles(cur_user.id)[:3]
        sorted_topics = get_sorted_topics(cur_user)

        ctx = {
            'user': cur_user,
            'users_articles': articles,
            'recommendation': articles_on_preferred_topics,
            'topics': Topic.objects.all(),
            'ordered_topics': sorted_topics,
        }

        return render(request, 'user_profile_page.html', ctx)
    except UserModel.DoesNotExist:
        raise Http404('There is no such user.')


def set_password(request: HttpRequest, username) -> HttpResponse:
    try:
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        raise Http404
    if not request.user.is_authenticated:
        url = reverse('login_user')
        return HttpResponseRedirect(url)
    if request.method == "POST":
        form = SetNewPassword(request.POST, initial={'username': username})
        if form.is_valid():
            form.update_data(username)

            url = reverse('user:password_changed')
            return HttpResponseRedirect(url)
    else:
        form = SetNewPassword(initial={'username': username})
    return render(request, 'set_password.html', {"form": form})


def password_changed(request: HttpRequest) -> HttpResponse:
    return render(request, 'password_changed.html')


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


def deactivate(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        url = reverse('user:login_user')
        return HttpResponseRedirect(url)
    user = request.user
    if request.method == "POST":
        logout(request)
        user.is_active = False
        user.save()
        url = reverse('user:login_user')
        return HttpResponseRedirect(url)
    return render(request, 'deactivate.html')


def reactivate(request):
    if request.method == "POST":
        form = Reactivate(request.POST)
        if form.is_valid():
            form.reactivate()

            url = reverse('user:success_reactivation')
            return HttpResponseRedirect(url)
    else:
        form = RegistrateUser()
    return render(request, 'reactivate.html', {"form": form})


def success_reactivation(request):
    return render(request, 'success_reactivation.html')


def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrateUser(request.POST)
        if form.is_valid():
            form.create_user()

            url = reverse('user:login_user')
            return HttpResponseRedirect(url)
    else:
        form = RegistrateUser()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = LoginUser(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            login(request, user)

            url = reverse('user:profile_page', kwargs={'username': user.username})
            return HttpResponseRedirect(url)
    else:
        form = LoginUser()

    return render(request, 'login.html', {'form': form})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    url = reverse('main_page')
    return HttpResponseRedirect(url)
