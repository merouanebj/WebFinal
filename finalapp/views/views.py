from django.shortcuts import get_object_or_404, redirect, render
from finalapp.forms import *
from finalapp.models import *
from django.contrib import messages
from serpapi import GoogleSearch
from django.contrib.auth.decorators import login_required, permission_required
from finalapp.decorators import check_user_ability


def Test(request):
    return render(request, 'main.html')


def ApiData(pk):  # l'id du chercheur
    r = Researcher.objects.get(pk=pk)
    params = {
        "engine": "google_scholar_author",
        "author_id": r.get_google_id(),
        "api_key": "efa8d7e7a7fda118b855de81e82288b21f5c99811905b85a22e9dfc84ebbae4d"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


@login_required
@check_user_ability("chef_division")
def home_views(request):
    chercheurs = Researcher.objects.all()
    divisions = Division.objects.all()
    Etablisments = Etablisment.objects.all()
    Total_chercheur = chercheurs.count() - 1
    Total_Etablisment = Etablisments.count()
    Total_division = divisions.count() - 1
    context = {
        'Total_chercheur': Total_chercheur,
        'Total_Etablisment': Total_Etablisment,
        'Total_division': Total_division
    }
    return render(request, 'home.html', context)

# ------------------------------------------------------------------------------------
# Etablisment


@permission_required('finalapp.add_etablisement')
def creat_Etablisment_views(request):
    form = EtablismentForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Etablisment a été ajouté avec succée')
            return redirect("creatEtablisment")
        return render(request, "creatEtablisment.html", {"form": form})

    else:
        form = EtablismentForm
        return render(request, 'creatEtablisment.html', {"form": form})

# Modifier


def update_Etablisment_views(request, pk):
    cher = get_object_or_404(Etablisment, pk=pk)
    form = EtablismentForm(instance=cher)
    if request.method == "POST":
        form = EtablismentForm(request.POST, instance=cher)
        if form.is_valid():
            form.save()
            return redirect('', pk=pk)

    context = {'form': form}
    return render(request, 'updateEta.html', context)
# Supprimer


def Delete_Etablisment_views(request, pk):
    Etu = Etablisment.objects.get(id=pk)
    Etu.delete()
    return redirect('home')  # il faut retourner HttpTesponse

# Liste des Etablismet
# tout


def EtablismentList():
    i = Etablisment.objects.all()
    return i

# le nombre d'eta par wilaya


def EtablismentList_location(pk):  # l'id d'une wilaya
    i = Etablisment.objects.filter(location=pk)
    return i

# ----------------------------------------------------------
# Division
# Ajouter


def creat_division_views(request):
    form = DivisionForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Division a été ajouté avec succée')
            return redirect("creatDivision")
        return render(request, "creatDivision.html", {"form": form})

    else:
        form = DivisionForm
        return render(request, 'creatDivision.html', {"form": form})

# Modifier


def update_division_views(request, pk):
    cher = get_object_or_404(Division, pk=pk)
    form = DivisionForm(instance=cher)
    if request.method == "POST":
        form = DivisionForm(request.POST, instance=cher)
        if form.is_valid():
            form.save()
            return redirect('G_chercheurs')

    context = {'form': form}
    return render(request, 'updateDiv.html', context)

# Supprimer


def Delete_division_views(request, pk):
    Etu = Division.objects.get(id=pk)
    Etu.delete()
    return redirect('G_chercheurs')

# List des Division
# tout les Division


def DivisionList():
    i = Division.objects.all()
    return i


def DivsionList_Eta(pk):
    i = Division.objects.filter(etablisment=pk)
    return i

# --------------------------------------------------------
# Equipe
# Ajouter


def creat_equipe_views(request):
    idc = ""
    form = EquipeForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipe a été ajouté avec succée')
            return redirect("createquipe")

        context = {"form": form}
        return render(request, "createquipe.html", context)

    else:

        context = {"form": form, 'idc': idc}
        form = EquipeForm
        return render(request, 'createquipe.html', context)

# Modifier


def update_equipe_views(request, pk):
    bj = get_object_or_404(Equipe, pk=pk)
    form = EquipeForm(instance=bj)
    if request.method == "POST":
        form = EquipeForm(request.POST, instance=bj)
        if form.is_valid():
            form.save()
            return redirect('G_chercheurs')

    return render(request, 'updateEquipe.html', {'form': form})
# Supprimer


def Delete_equipe_views(request, pk):
    Etu = Equipe.objects.get(id=pk)
    Etu.delete()
    return redirect('G_chercheurs')

# List des equipe
# tout les equipe


def EquipeList():
    i = Equipe.objects.all()
    return i

# Les equipe d'un Etablisment


def EquipeList_Eta(pk):  # pk d'un Etablismet
    inter = Division.objects.filter(etablisment=pk)
    researchers = Laboratoire.objects.none()
    inter3 = []

    for i in inter:
        researchers = Laboratoire.objects.filter(division=i.id)
        inter3 += researchers
    i = []
    for i1 in inter:
        researchers = Equipe.objects.filter(laboratoire=i1.id)
        i += researchers
    return i

# Les equipe d'un Division


def EquipeList_Div(pk):  # pk d'un Division
    inter = Laboratoire.objects.filter(division=pk)
    researchers = Equipe.objects.none()
    i = []
    for i1 in inter:
        researchers = Equipe.objects.filter(laboratoire=i1.id)
        i += researchers
    return i

# Les equipe d'un Laboratoire


def EquipeList_Lab(pk):  # pk d'un labo
    i = Equipe.objects.filter(laboratoire=pk)
    return i

# -------------------------------------------------------------------
# Chercheur
# les information pour un profil de chercheur


def CherList_equipe(request, pk):  # pk represent l'id de l'equipe (rest a test)
    researchers = Researcher.objects.filter(equipe_researchers=pk)
    return researchers

# afficher les chercheur d'un laboratoire


def CherList_labo(request, pk):

    inter = Equipe.objects.filter(laboratoire=pk)
    researchers = Researcher.objects.none()
    inter2 = []
    for i in inter:
        researchers = Researcher.objects.filter(equipe_researchers=i.id)

        inter2 += researchers

    return inter2

# afficher les chercheur d'un division


def CherList_div(request, pk):
    inter = Laboratoire.objects.filter(division=pk)
    interEquipe = Equipe.objects.none()
    inter2 = []
    for i in inter:
        interEquipe = Equipe.objects.filter(laboratoire=i.id)
        inter2 += interEquipe

    final = []
    for i in inter2:
        researchers = Researcher.objects.filter(equipe_researchers=i.id)
        final += researchers

    return final

# afficher les chercheur d'un  Etablisment


def CherList_eta(request, pk):
    inter = Division.objects.filter(etablisment=pk)
    interLaboratoire = Equipe.objects.none()
    inter3 = []
    # recuperation des Laboratoire
    for i in inter:
        interLaboratoire = Laboratoire.objects.filter(division=i.id)
        inter3 += interLaboratoire
    # recuperation des Equipe
    inter2 = []
    for i in inter3:
        interEquipe = Equipe.objects.filter(laboratoire=i.id)
        inter2 += interEquipe
    # recuperation des chercheur
    final = []
    for i in inter2:
        researchers = Researcher.objects.filter(equipe_researchers=i.id)
        final += researchers

    return final


def Profil_views(request):
    chercheur1 = Researcher.objects.get(id=request.user.pk)
    # pour recuperer les donnes
    chercheur = Researcher.objects.filter(id=request.user.pk)
    # equipe = Equipe.objects.filter(id=chercheur[0].equipe_researchers.id)
    # laboratoire = Laboratoire.objects.filter(id=equipe[0].laboratoire.id)
    # division = Division.objects.filter(id=laboratoire[0].division.id)
    # etablisment = Etablisment.objects.filter(id=division[0].etablisment.id)
    # apiData = ApiData(request.user.pk)
    # context = {'chercheur1': chercheur1, 'apiData': apiData, 'etablisment': etablisment,
    #            'equipe': equipe, 'laboratoire': laboratoire, 'division': division, 'equipe': equipe}

    context = {}
    return render(request, 'profil.html', context)


def Profil_views_externe(request, pk):
    chercheur1 = Researcher.objects.get(id=pk)
    # pour recuperer les donnes
    chercheur = Researcher.objects.filter(id=pk)
    equipe = Equipe.objects.filter(id=chercheur[0].equipe_researchers.id)
    laboratoire = Laboratoire.objects.filter(id=equipe[0].laboratoire.id)
    division = Division.objects.filter(id=laboratoire[0].division.id)
    etablisment = Etablisment.objects.filter(id=division[0].etablisment.id)
    context = {'chercheur1': chercheur1, 'etablisment': etablisment, 'equipe': equipe,
               'laboratoire': laboratoire, 'division': division, 'equipe': equipe}
    return render(request, 'profil.html', context)


def Delete_Cher_views(request, pk):
    Etu = Researcher.objects.get(id=pk)
    Etu.delete()
    # la page li nekonon fiha nekhedmo bel confirme
    return redirect('G_chercheurs')


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

    moy_indice_h = moy_indice_h/nbr_cher_equipe
    moy_indice_i10 = moy_indice_i10/nbr_cher_equipe

    context = {'nbr_cher_equipe': nbr_cher_equipe, 'info_equipe': info_equipe,
               'nbr_Citation': nbr_Citation, 'moy_indice_h': moy_indice_h, 'moy_indice_i10': moy_indice_i10}
    return context


def Dash_Laboratoire_calc(pk):
    info_laboratoire = Laboratoire.objects.get(pk=pk)
    equipes = Equipe.objects.filter(laboratoire=pk)
    nbr_equipe_laboratoire = equipes.count()
    nbr_CitationL = 0
    nbr_cher_laboratoire = 0
    moy_indice_hL = 0.0
    moy_indice_i10L = 0.0
    for i in equipes:
        inter = Dash_Equipe_calc(i.id)
        nbr_CitationL += inter["nbr_Citation"]
        moy_indice_hL += inter["moy_indice_h"]
        moy_indice_i10L += inter["moy_indice_i10"]
        nbr_cher_laboratoire += inter["nbr_cher_equipe"]

    moy_indice_hL = moy_indice_hL/nbr_equipe_laboratoire
    moy_indice_i10L = moy_indice_i10L/nbr_equipe_laboratoire

    context = {'nbr_equipe_laboratoire': nbr_equipe_laboratoire, 'nbr_cher_laboratoire': nbr_cher_laboratoire,
               'info_laboratoire': info_laboratoire, 'nbr_Citation': nbr_CitationL, 'moy_indice_h': moy_indice_hL, 'moy_indice_i10': moy_indice_i10L}
    return context


def Dash_Equipe(request, pk):
    context = Dash_Equipe_calc(pk)
    return render(request, 'DashEquipe.html', context)


def Dash_Laboratoire(request, pk):
    context = Dash_Laboratoire_calc(pk)
    return render(request, 'DashLaboratoire.html', context)


def Recup_id(request):
    i = Researcher.objects.get(pk=request.user.id)
    equipe_id = Equipe.objects.get(pk=i.equipe_researchers.id)
    laboratoire_id = Laboratoire.objects.get(pk=equipe_id.laboratoire.id)
    division_id = Division.objects.get(id=laboratoire_id.division.id)
    etablisment_id = Etablisment.objects.get(id=division_id.etablisment.id)
    context = {
        'equipe_id': equipe_id,
        'laboratoire_id': laboratoire_id,
        'division_id': division_id,
        'etablisment_id': etablisment_id
    }
    return context


# affichage des listes de chercheur

def Liste_cher_Eta_aff(request):
    inter = Recup_id(request)
    inter2 = inter["etablisment_id"]
    liste = CherList_eta(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_eta.html', context)


def Liste_cher_Div_aff(request):
    inter = Recup_id(request)
    inter2 = inter["division_id"]
    liste = CherList_div(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_div.html', context)


def Liste_cher_Lab_aff(request):
    inter = Recup_id(request)
    inter2 = inter["laboratoire_id"]
    liste = CherList_labo(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_lab.html', context)


def Liste_cher_Equipe_aff(request):
    inter = Recup_id(request)
    inter2 = inter["equipe_id"]
    liste = CherList_equipe(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_equipe.html', context)


# les affichage d'une chef d'equipe
    # DashEquipe
    # Liste Chercheur


def Liste_cher_Equipe_aff(request):
    inter = Recup_id(request)
    inter2 = inter["equipe_id"]
    liste = CherList_equipe(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_equipe.html', context)

# les affichage d'une chef de labo

    # DashLabo
    # Liste Equipe labo
    # Liste chercheur labo

# les affichage d'une chef Divsion
    # Dash Divsion
    # Liste labo
    # Liste Equipe
    # Liste chercheur

# les affichage d'une chef Divsion
    # Dash Divsion
    # Liste labo
    # Liste Equipe
    # Liste chercheur

# les affichage d'une chef Etablisment
    # Dash Etablismet
    # liste division
    # Liste labo
    # Liste Equipe
    # Liste chercheur

  # DashLabo


def Dash_Laboratoire(request, pk):
    context = Dash_Laboratoire_calc(pk)
    return render(request, 'DashLaboratoire.html', context)
  # Liste Equipe labo


def Liste_equipe_Lab_aff(request):
    inter = Recup_id(request)
    inter2 = inter["laboratoire_id"]
    liste = EquipeList_Lab(request, inter2)
    context = {'liste': liste}
  # Liste chercheur labo


def Liste_cher_Lab_aff(request):
    inter = Recup_id(request)
    inter2 = inter["laboratoire_id"]
    liste = CherList_labo(request, inter2)
    context = {'liste': liste}
    return render(request, 'list_ch_lab.html', context)


def Recup_id_etablisment(request):
    i = Researcher.objects.get(pk=request.user.id)
    equipe_id = Equipe.objects.get(pk=i.equipe_researchers.id)
    laboratoire_id = Laboratoire.objects.get(pk=equipe_id.laboratoire.id)
    division_id = Division.objects.get(id=laboratoire_id.division.id)
    etablisment_id = Etablisment.objects.get(id=division_id.etablisment.id)
    context = {
        'etablisment_id': etablisment_id
    }
    return context


# test chef lab


def TestChefLaboratoire(reqeust):
    inter = Recup_id_laboratoire(reqeust)
    inter2 = inter["laboratoire_id"]
    equipe = Laboratoire.objects.filter(id=inter2)
    if equipe.chef_labo.id == reqeust.user.id:
        return True
    return False

# test chef Divison


def TestChefDivsion(reqeust):
    inter = Recup_id_division(reqeust)
    inter2 = inter["division_id"]
    equipe = Division.objects.filter(id=inter2)
    if equipe.chef_div.id == reqeust.user.id:
        return True
    return False


def TestChefDivsion(reqeust):
    inter = Recup_id_etablisment(reqeust)
    inter2 = inter["etablisment_id"]
    equipe = Etablisment.objects.filter(id=inter2)
    if equipe.chef_etablisement.id == reqeust.user.id:
        return True
    return False
