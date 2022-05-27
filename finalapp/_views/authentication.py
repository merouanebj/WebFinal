from django.shortcuts import *
from finalapp.models import *
from finalapp.forms import *
from django.contrib.auth import authenticate, login, logout, decorators
from finalapp.decorators import *


def Register_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    # wilaya = Location.objects.all()
    # etablisment= Etablisment.objects.all()
    # division= Division.objects.all()
    # laboratoire= Laboratoire.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            user1 = form.cleaned_data.get('last_name')
            messages.success(request, 'Compte cree pour '+user + ' '+user1)
            return redirect('login')
        # messages.error(request,'Verifier les inforamation fournit ')
    context = {'form': form}
    #    'etablisment':etablisment,
    #    'wilaya':wilaya,
    #    'laboratoire':laboratoire ,
    #    'division':division}

    return render(request, 'register.html', context)


def Logout_views(request):
    logout(request)
    return redirect('login')


@redirect_logged_in_user
def Login_views(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Email ou Mot de passe incorect')
    context = {}
    return render(request, 'login.html', context)
