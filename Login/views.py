from django.shortcuts import render
from .froms import UserForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.


def login_page(request):
    context = {}
    return render(request, 'login_app/login.html', context=context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('login:index'))
            else:
                return HttpResponse("Your account is not active!!")

        else:
            return HttpResponse("Username or Password is wrong!!")

    else:
        return HttpResponseRedirect(reverse('login:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))


@login_required
def index(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_info = User.objects.get(pk=user_id)
        user_more_info = UserProfile.objects.get(user__pk=user_id)
        users = User.objects.all()
        information = UserProfile.objects.all()
        context = {'title': 'Home', 'users': users, 'profile': information, 'user_info': user_info,
                   'user_more_info': user_more_info}

    return render(request, 'login_app/index.html', context=context)


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user

            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']

            user_profile.save()
            registered = True

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context = {'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered}
    return render(request, 'login_app/registration.html', context=context)