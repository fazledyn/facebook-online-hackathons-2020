from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#Forms
from django.contrib.auth.forms import UserCreationForm
# Custom App Imports

# Create your views here.
def index(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("username: ", username, " password: ", password)
            return redirect('dashboard')

    return render(request, 'index.html')

@login_required
def dashboard(request):
    return HttpResponse("Dashboard here")


@login_required
def site_logout(request):
    logout(request)
    return redirect('index')


def signup(request):
    error_messages = []

    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2 and len(password1) >= 8:
            new_user = User.objects.create_user(username=username, password=password1)
            new_user.save()
            print("new user creatd !")

            return redirect('index')

        if username == password1:
            error_messages.append("Username and password can't be same !")

        if len(password1) < 8:
            error_messages.append("Passwords must be 8 character long")

        if password1 != password2:
            error_messages.append("Passwords don't match !")

        if User.objects.filter(username=username) is None:
            error_messages.append("User already exists !")

    context = {'errors': error_messages}
    return render(request, 'signup.html', context)



