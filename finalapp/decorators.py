
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from finalapp.models import Division, Equipe, Researcher


def check_user_group(*groups):
    def decorators(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request)
            return HttpResponse('you dont have acces')
        return wrapper
    return decorators


def redirect_logged_in_user(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect("profile")
        else:
            return func(request)
    return wrapper


def check_if_chefequipe(function):
    def wrapper(request, pk):
        if request.user == Equipe.objects.get(id=pk).chef_equipe:
            return function(request, pk)
        raise Http404("You dont have access")
    return wrapper


def check_division_chef(function):
    def wrapper(request):
        if request.user.pk == Division.objects.get():
            pass


def check_user_identity(function):
    def wrapper(request, pk):
        if not Researcher.objects.get(id=request.user.pk).equipe_researchers_id == Researcher.objects.get(id=pk).equipe_researchers_id:
            return HttpResponse('you dont have acces')
        return function(request, pk)
    return wrapper


def check_if_chefdivision(function):
    def wrapper(request):
        if not Division.objects.filter(chef_div__id=request.user.pk):
            return HttpResponse('you dont have acces')
        return function(request)
    return wrapper
