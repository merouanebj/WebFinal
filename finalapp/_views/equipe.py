from django.shortcuts import render
from finalapp.models import *
from finalapp._views.views import *
from finalapp.decorators import *
from django.contrib.auth.decorators import login_required
from finalapp._views.functions import *
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


@login_required
# @check_if_chefequipe
def equipe_members(request):
    context = {}
    context["members"] = get_equipe_members(request)
    return render(request, 'pages/equipe/equipe_members.html', context)


@login_required
# @check_if_chefequipe
def equipe_dashboard(request):
    context = {}
    nbr_members = nbr_equipe_members(get_equipe_pk(request))
    members = get_equipe_members(request)
    h_index_total = 0
    i10_index_total = 0
    citation_total = 0
    final_8years_citations_total = [
        {"year": 2015, "citations": 0},
        {"year": 2016, "citations": 0},
        {"year": 2017, "citations": 0},
        {"year": 2018, "citations": 0},
        {"year": 2019, "citations": 0},
        {"year": 2020, "citations": 0},
        {"year": 2021, "citations": 0},
        {"year": 2022, "citations": 0},
    ]
    for member in members:
        member_gs = serpapi_author(member.get_google_id())
        citation_total += member_gs["cited_by"]["table"][0]["citations"]["all"]
        h_index_total += member_gs["cited_by"]["table"][1]["h_index"]["all"]
        i10_index_total += member_gs["cited_by"]["table"][2]["i10_index"]["all"]
        for i in range(0, 7):
            graph = member_gs["cited_by"]["graph"]
            year = final_8years_citations_total[i]["year"]
            final_8years_citations_total[i]["citations"] += next(
                filter(lambda x: x["year"] == year, graph))["citations"]
            print(final_8years_citations_total[i]["citations"])
            print("ok")
            print(next(filter(lambda x: x["year"] == year, graph))[
                  "citations"])

    context["nbr_members"] = nbr_members
    context["h_index_total"] = h_index_total
    context["i10_index_total"] = i10_index_total
    context["citation_total"] = citation_total
    context["final_8years_citations_total"] = final_8years_citations_total

    return render(request, 'pages/equipe/equipe_dash.html', context)
