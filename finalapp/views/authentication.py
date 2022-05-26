from django.shortcuts import redirect, render
from finalapp.forms import *
from django.contrib.auth import authenticate, login, logout
from finalapp.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from finalapp.admin import UserCreationForm


def Register_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            user1 = form.cleaned_data.get('last_name')
            messages.success(request, 'Compte cree pour '+user + ' '+user1)
            Login_views(request)
            return redirect('profil')
    context = {'form': form}
    return render(request, 'register.html', context)


def Logout_views(request):
    logout(request)
    return redirect('login')


def Login_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profil')
        else:
            messages.info(request, 'Email ou Mot de passe incorect')
    context = {}
    return render(request, 'login.html', context)
