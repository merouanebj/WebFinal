from atexit import register
import email
from multiprocessing import context
from pyexpat.errors import messages
import re
from django.shortcuts import get_object_or_404, redirect, render
import requests
from .forms import *
from  django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages

# Create your views here.
#Login
def Register_views(request):
    if request.user.is_authenticated:
        return redirect('createquipe')
    wilaya = Location.objects.all()
    etablisment= Etablisment.objects.all()
    division= Division.objects.all()
    laboratoire= Laboratoire.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            user1 = form.cleaned_data.get('last_name')
            messages.success(request,'Compte cree pour '+user +''+user1)
            return redirect('login')
        messages.error(request,'Verifier vous information n\'oublier pas que')      
    context = {'form':form,               
               'etablisment':etablisment,
               'wilaya':wilaya,
               'laboratoire':laboratoire ,
               'division':division}

    return render (request,'register.html',context)

def Login_views(request):
    if request.user.is_authenticated:
        return redirect('createquipe')
    if request.method == 'POST':
        email =request.POST.get('email')
        password = request.POST.get('password')
        
        user =authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('landing')
        else:
            messages.info(request,'Email ou Mot de passe incorect')
    context = {}
    return render (request,'login.html',context)
   

def ApiData(pk): # l'id du chercheur
    researchers  = Researcher.objects.filter(pk = pk)
    API ="https://serpapi.com/search.json?engine=google_scholar_author&author_id=LSsXyncAAAAJ&hl&api_key=b4c86099edf995eae27b4b1fde352761f65bf5cc39610783615a1382c05a33d4"
    merouane = API.replace('LSsXyncAAAAJ',str(researchers[0].google_scholar_account[42:]))
    response = requests.get(merouane).json()
    citation=0
    index_h=0
    index_i10 = 0
    citation=response["cited_by"]["table"][0]["citations"]["all"]
    index_h=response["cited_by"]["table"][1]["h_index"]["all"]  
    index_i10=response["cited_by"]["table"][2]["i10_index"]["all"]
    context ={
    'citation':citation,
    'index_h':index_h,
    'index_i10':index_i10,  
    }    
    return  context


def home_views(request):
   labos = Laboratoire.objects.all()
   chercheurs =Researcher.objects.all()
   divisions = Division.objects.all()
   Etablisments =Etablisment.objects.all()  
    
    
    
   Total_labo =labos.count() - 1
   Total_chercheur =chercheurs.count()- 1
   Total_Etablisment = Etablisments.count() 
   Total_division=  divisions.count() - 1
   context = {
                'Total_labo':Total_labo,
                'Total_chercheur':Total_chercheur,
                'Total_Etablisment':Total_Etablisment,
                'Total_division':Total_division
                 } 
   return render(request,'home.html',context)

# ------------------------------------------------------------------------------------
#Etablisment
def creat_Etablisment_views(request):
    form =EtablismentForm(data=request.POST)
    if request.method =="POST":     
        if form.is_valid() :
             form.save()
             messages.success(request, 'Etablisment a été ajouté avec succée')
             return redirect("creatEtablisment")
        return render(request,"creatEtablisment.html",{"form":form})

    else:
           form=EtablismentForm
           return render(request,'creatEtablisment.html',{"form":form})

#Modifier
def update_Etablisment_views(request,pk):
    cher = get_object_or_404(Etablisment, pk=pk)
    form =EtablismentForm(instance=cher)
    if request.method =="POST":   
        form =EtablismentForm(request.POST,instance=cher)
        if form.is_valid():
             form.save()
             return redirect('', pk=pk)

    context = {'form':form}
    return render(request,'updateEta.html',context)
#Supprimer
def Delete_Etablisment_views (request,pk):
    Etu=Etablisment.objects.get(id=pk)
    Etu.delete()
    return redirect('home') # il faut retourner HttpTesponse

#Liste des Etablismet 
#tout
def EtablismentList():
    i = Etablisment.objects.all()
    return i

# le nombre d'eta par wilaya 
def EtablismentList_location(pk):# l'id d'une wilaya
    i = Etablisment.objects.filter(location = pk)
    return i

#----------------------------------------------------------
#Division
#Ajouter
def creat_division_views(request):
    form =DivisionForm(data=request.POST)
    if request.method =="POST":   
        if form.is_valid() :
             form.save()
             messages.success(request, 'Division a été ajouté avec succée')
             return redirect("creatDivision")
        return render(request,"creatDivision.html",{"form":form})

    else:
           form= DivisionForm
           return render(request,'creatDivision.html',{"form":form})

#Modifier
def update_division_views(request,pk):
    cher = get_object_or_404(Division, pk=pk)
    form =DivisionForm(instance=cher)
    if request.method =="POST":   
        form =DivisionForm(request.POST,instance=cher)
        if form.is_valid():
             form.save()
             return redirect('G_chercheurs')

    context = {'form':form}
    return render(request,'updateDiv.html',context)

#Supprimer
def Delete_division_views (request,pk):
    Etu=Division.objects.get(id_author=pk)
    Etu.delete()
    return redirect('G_chercheurs')  

# List des Division
# tout les Division
def DivisionList(): 
    i = Division.objects.all()
    return i

# les laboratoire d'une division
def DivsionList_Eta(pk):
    i = Division.objects.filter(etablisment = pk)
    return i

#----------------------------------------------------------------
#Laboratoire
def creat_labo_views(request):
    form =LaboratoireForm(data=request.POST)
    if request.method =="POST":   
        if form.is_valid() :
             form.save()
             messages.success(request, 'Laboratoire a été ajouté avec succée')
             return redirect("creatlabo")
        return render(request,"creatlabo.html",{"form":form})

    else:
           form= LaboratoireForm
           return render(request,'creatlabo.html',{"form":form})   

#Modifier
def update_laboratoire_views(request,pk):
    cher = get_object_or_404(Laboratoire, pk=pk)
    form =LaboratoireForm(instance=cher)
    if request.method =="POST":   
        form =LaboratoireForm(request.POST,instance=cher)
        if form.is_valid():
             form.save()
             return redirect('G_chercheurs')

    context = {'form':form}
    return render(request,'updateLab.html',context) 

#Supprimer
def Delete_laboratoire_views (request,pk):
    Etu=Laboratoire.objects.get(id_author=pk)
    Etu.delete()
    return redirect('G_chercheurs')      

# List des laboratoire
# tout les laboratoire
def LaboratoireList(): 
    i = Laboratoire.objects.all()
    return i

# les laboratoire d'un division
def LaboratoireList_Div(pk):
    i = Laboratoire.objects.filter(division = pk)
    return i

#les laboratoire d'un Eta
def LaboratoireList_Eta(pk):
    inter = Division.objects.filter(etablisment = pk)
    researcher = Laboratoire.objects.none()
    i =[]
    for i1 in inter:
        researcher = Laboratoire.objects.filter(division = i1.id)
        i +=researcher
    return i  
#--------------------------------------------------------
#Equipe
#Ajouter
def creat_equipe_views(request):
    form =EquipeForm(data=request.POST)
    if request.method =="POST":   
        if form.is_valid() :
             form.save()
             messages.success(request, 'Equipe a été ajouté avec succée')
             return redirect("createquipe")
        i=ApiData(1)
        context={"form":form,'i':i}
        return render(request,"createquipe.html",context)

    else:   
           i=ApiData(1)
           context={"form":form,'i':i}
           form= EquipeForm
           return render(request,'createquipe.html',context)

#Modifier
def update_equipe_views(request,pk):
    bj = get_object_or_404(Equipe,pk=pk)
    form =EquipeForm(instance = bj)
    if request.method =="POST":   
        form =EquipeForm(request.POST,instance=bj)
        if form.is_valid():
             form.save()
             return redirect('G_chercheurs')
    
    return render(request,'updateEquipe.html',{'form':form})
#Supprimer

def Delete_equipe_views (request,pk):
    Etu=Equipe.objects.get(id_author=pk)
    Etu.delete()
    return redirect('G_chercheurs')

# List des equipe
#tout les equipe
def EquipeList(): 
    i = Equipe.objects.all()
    return i

#Les equipe d'un Etablisment
def EquipeList_Eta(pk):#pk d'un Etablismet
    inter = Division.objects.filter(etablisment = pk)
    researchers = Laboratoire.objects.none()
    inter3  =[]

    for i in inter:
       researchers = Laboratoire.objects.filter(division = i.id)
       inter3 +=researchers
    i=[]
    for i1 in inter:
       researchers = Equipe.objects.filter(laboratoire = i1.id)
       i +=researchers
    return i
  
#Les equipe d'un Division
def EquipeList_Div(pk):#pk d'un Division
    inter = Laboratoire.objects.filter(division = pk)
    researchers = Equipe.objects.none()
    i =[]
    for i1 in inter:
       researchers = Equipe.objects.filter(laboratoire = i1.id)
       i +=researchers
    return i

#Les equipe d'un Laboratoire
def EquipeList_Lab(pk):#pk d'un labo
    i = Equipe.objects.filter(laboratoire = pk)
    return i

#-------------------------------------------------------------------
#Chercheur
# les information pour un profil de chercheur

#Ajax
def load_etablisments(request):
    wilaya_id = request.GET.get('wilaya_id')
    etablisments = Etablisment.objects.filter(wilaya_id=wilaya_id).all()
    return render(request, 'etablisments_dropdown_list_options.html', {'etablisments': etablisments})

def load_divisions(request):
    etablisment_id = request.GET.get('etablisment_id')
    divisions = Division.objects.filter(etablisment_id=etablisment_id).all()
    return render(request, 'divisions_dropdown_list_options.html', {'divisions': divisions})

def load_labos(request):
    division_id = request.GET.get('division_id')
    labos = Laboratoire.objects.filter(division=division_id).all()
    return render(request, 'labos_dropdown_list_options.html', {'labos': labos})

def load_equipes(request):
    labo_id = request.GET.get('labo_id')
    equipes = Equipe.objects.filter(labo_id=labo_id).all()
    return render(request, 'equipes_dropdown_list_options.html', {'equipes': equipes})