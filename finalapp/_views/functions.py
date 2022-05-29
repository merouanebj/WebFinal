from serpapi import GoogleSearch
from finalapp.models import *


def serpapi_author(researcher_id):
    params = {
        "engine": "google_scholar_author",
        "author_id": researcher_id,
        "api_key": "bfdde7462931844d6003e1d183494fad96f1011bdd6d192179f5bae85d0e16c1"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


def check_google_scholar_id(gs_id):
    params = {
        "engine": "google_scholar_author",
        "author_id": gs_id,
        "api_key": "bfdde7462931844d6003e1d183494fad96f1011bdd6d192179f5bae85d0e16c1"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "author" in results:
        return True
    return False


def check_if_equipe_memebre(request):
    if Researcher.objects.get(id=request.user.pk).equipe_researchers:
        return True
    return False


def check_if_chef_equipe(request):
    if request.user.pk == Equipe.objects.get(id=request.user.id).chef_equipe.id:
        return True
    return False


def check_if_chefdiv(request):
    if request.user.pk == Division.objects.get(id=request.user.pk).chef_div.id:
        return True
    return False


def check_if_chef_etablisement(request):
    if request.user.pk == Etablisment.objects.get(id=request.user.pk).chef_etablisement_id:
        return True
    return False

# MESRS/DGRSDT/CNRS


def check_if_superuser(request):
    if request.user.is_superuser:
        return True
    return False


def nbr_equipe_members(id):
    return len(list(Equipe.objects.filter(id=id)))


def get_equipe_pk(request):
    return Equipe.objects.get(chef_equipe_id=request.user.pk).id


def get_equipe_members(request):
    return list(Researcher.objects.filter(equipe_researchers=get_equipe_pk(request)))
