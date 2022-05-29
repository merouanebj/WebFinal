from django.http import HttpResponse
from django.shortcuts import render
from finalapp.views import *
from finalapp._views.functions import *


def try_view(request):
    context = {}
    context["data"] = serpapi_author(request)["cited_by"]["graph"]
    return render(request, 'pages/equipe.html', context)


def equipe_dash(request):
    context = {}
    members = list(Researcher.objects.filter(
        equipe_researchers__id=request.user.pk))
    num_members = len(list(Researcher.objects.filter(
        equipe_researchers__id=request.user.pk)))
    for i in range(0, num_members-1):
        pass
