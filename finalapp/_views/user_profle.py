from django.shortcuts import render
from finalapp.models import *
from finalapp.views import *
from finalapp.decorators import *
from django.contrib.auth.decorators import login_required
from serpapi import GoogleSearch


def serpapi_author(request):
    params = {
        "engine": "google_scholar_author",
        "author_id": Researcher.objects.get(id=request.user.id).get_google_id(),
        "api_key": "6bbac90594777b50d1a7cb232de4c87e7eab93ca2cbdf37657081d9912f28970"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


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


def check_if_equipe_memebre(request):
    if Researcher.objects.get(id=request.user.pk).equipe_researchers:
        return True
    return False


def user_profile(request):
    context = {}
    context["citations"] = serpapi_author(request)[
        "cited_by"]["table"][0]["citations"]["all"]
    context["h_index"] = serpapi_author(request)[
        "cited_by"]["table"][1]["h_index"]["all"]
    context["i10_index"] = serpapi_author(request)[
        "cited_by"]["table"][2]["i10_index"]["all"]
    context["graph"] = serpapi_author(request)["cited_by"]["graph"]

    equipe = Equipe.objects.filter(id=Researcher.objects.get(
        id=request.user.pk).equipe_researchers)
    print(equipe)
    context["equipe"] = equipe
    return render(request, 'modified/user_profile.html', context)
