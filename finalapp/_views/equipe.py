from django.shortcuts import render
from finalapp.models import *
from finalapp._views.views import *
from finalapp.decorators import *
from django.contrib.auth.decorators import login_required

# on fait sous form de fonction pour utulistaion direct dans les autre dash board


def Dash_Equipe_calc(pk):
    info_equipe = Equipe.objects.get(pk=pk)
    researchers = Researcher.objects.filter(
        equipe_researchers=pk)  # recupere les chercheur des equipe
    nbr_cher_equipe = researchers.count()
    nbr_Citation = 0
    moy_indice_h = 0.0
    moy_indice_i10 = 0.0
    for i in researchers:
        inter = ApiData(i.id)
        nbr_Citation += inter["cited_by"]["table"][0]["citations"]["all"]
        moy_indice_h += inter["cited_by"]["table"][1]["h_index"]["all"]
        moy_indice_i10 += inter["cited_by"]["table"][2]["i10_index"]["all"]
    if nbr_cher_equipe == 0:
        moy_indice_hs = 0.0
        moy_indice_i10s = 0.0
    else:
        moy_indice_h = moy_indice_h/nbr_cher_equipe
        moy_indice_i10 = moy_indice_i10/nbr_cher_equipe

    context = {'nbr_cher_equipe': nbr_cher_equipe, 'info_equipe': info_equipe,
               'nbr_Citation': nbr_Citation, 'moy_indice_h': moy_indice_h, 'moy_indice_i10': moy_indice_i10}
    return context


def Dash_Division_calc(pk):
    info_division = Division.objects.get(pk=pk)
    equipes = Equipe.objects.filter(division=pk)
    nbr_equipe_division = equipes.count()
    nbr_CitationL = 0
    nbr_cher_division = 0
    moy_indice_hL = 0.0
    moy_indice_i10L = 0.0
    for i in equipes:
        inter = Dash_Equipe_calc(i.id)
        nbr_CitationL += inter["nbr_Citation"]
        moy_indice_hL += inter["moy_indice_h"]
        moy_indice_i10L += inter["moy_indice_i10"]
        nbr_cher_division += inter["nbr_cher_equipe"]
    if nbr_equipe_division == 0:
        moy_indice_hL = 0.0
        moy_indice_i10L = 0.0
    else:
        moy_indice_hL = moy_indice_hL/nbr_equipe_division
        moy_indice_i10L = moy_indice_i10L/nbr_equipe_division

    context = {'nbr_equipe_division': nbr_equipe_division, 'nbr_cher_division': nbr_cher_division, 'info_division': info_division,
               'nbr_Citation': nbr_CitationL, 'moy_indice_h': moy_indice_hL, 'moy_indice_i10': moy_indice_i10L}
    return context


@login_required
@check_if_chefequipe
def Dash_Equipe(request, pk):
    context = Dash_Equipe_calc(pk)
    chef = TestChefEquipe(request)
    context["chef"] = chef
    return render(request, 'DashEquipe.html', context)


# @check_if_chefdivision
# def create_equipe(request):
#     if request.method == 'POST':
#         form = EquipeForm(request.POST)
#         if form.is_valid():
#             form.

def equipe_dash(request):
    ApiData()
    return render()
