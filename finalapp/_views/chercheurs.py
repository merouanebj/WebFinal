from finalapp.models import *
from django.shortcuts import redirect


def Delete_Cher_views(request, pk):
    Etu = Researcher.objects.get(id=pk)
    Etu.delete()
    return redirect('G_chercheurs')


def CherList_equipe(pk):  # pk represent l'id de l'equipe (rest a test)
    researchers = Researcher.objects.filter(equipe_researchers=pk)
    return researchers


def CherList_div(pk):
    inter = Equipe.objects.filter(division=pk)
    researchers = Researcher.objects.none()
    inter2 = []
    for i in inter:
        researchers = Researcher.objects.filter(equipe_researchers=i.id)
        inter2 += researchers
    return inter2


def CherList_eta(pk):
    inter = Division.objects.filter(etablisment=pk)
    interEquipe = Equipe.objects.none()
    inter2 = []
    for i in inter:
        interEquipe = Equipe.objects.filter(division=i.id)
        inter2 += interEquipe
    final = []
    for i in inter2:
        researchers = Researcher.objects.filter(equipe_researchers=i.id)
        final += researchers
    return final
