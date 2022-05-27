from django.shortcuts import render
from finalapp.models import *
from finalapp.views import *
from finalapp.decorators import *
from django.contrib.auth.decorators import login_required


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
