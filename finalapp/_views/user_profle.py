from django.shortcuts import render
from finalapp.models import *
from finalapp._views.views import *
from finalapp.decorators import *
from django.contrib.auth.decorators import login_required
from .functions import *

# @check_user_group("chef_equipe")


def Profil_views(request):
    chercheur1 = Researcher.objects.get(id=request.user.pk)
    chercheur = Researcher.objects.filter(id=request.user.pk)
    equipe = Equipe.objects.filter(id=chercheur[0].equipe_researchers.id)
    division = Division.objects.filter(id=equipe[0].division.id)
    etablisment = Etablisment.objects.filter(id=division[0].etablisment.id)
    apiData = ApiData(request.user.pk)
    context = {'chercheur1': chercheur1, 'apiData': apiData,
               'etablisment': etablisment, 'division': division, 'equipe': equipe}
    return render(request, 'profil.html', context)


def user_profile(request):
    context = {}
    researcher_gs_id = Researcher.objects.get(
        id=request.user.id).get_google_id()
    if check_google_scholar_id(researcher_gs_id):
        context["citations"] = serpapi_author(researcher_gs_id)[
            "cited_by"]["table"][0]["citations"]["all"]
        context["h_index"] = serpapi_author(researcher_gs_id)[
            "cited_by"]["table"][1]["h_index"]["all"]
        context["i10_index"] = serpapi_author(researcher_gs_id)[
            "cited_by"]["table"][2]["i10_index"]["all"]
        context["graph"] = serpapi_author(researcher_gs_id)[
            "cited_by"]["graph"]
    else:
        context["error"] = "Check your google scholar account, No Data found"
    # equipe = Equipe.objects.filter(id=Researcher.objects.get(
    #     id=request.user.pk).equipe_researchers.id)
    # print(equipe)
    # context["equipe"] = equipe
    return render(request, 'pages/user_profile.html', context)
