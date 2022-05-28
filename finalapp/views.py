from __future__ import division
from pyexpat.errors import messages
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from finalapp.forms import *
from finalapp.models import *
from django.contrib import messages
from serpapi import GoogleSearch


def Test (request):
    return render (request,'main.html')
   

def ApiData(pk): # l'id du chercheur
    r  = Researcher.objects.get(pk = pk)
    params = {
    "engine": "google_scholar_author",
    "author_id": r.get_google_id(),
    "api_key": "5693539bbd7f27e4de0624ca01bc9ad9ecba73199cbc2ce132e589daa15f8e4a",
    "start": 0,
    "num": "100"
}
    search = GoogleSearch(params)
    results = search.get_dict()
    if results == {'error': 'Your searches for the month are exhausted. You can upgrade plans on SerpApi.com website.'}:
        results ={}
    else:    
       articles_num = len(results["articles"])
       flag = 100
       while "articles" in results:
         params = {
           "engine": "google_scholar_author",
           "author_id": r.get_google_id(),
           "api_key": "5693539bbd7f27e4de0624ca01bc9ad9ecba73199cbc2ce132e589daa15f8e4a",
           "start": flag,
           "num": str(flag+100)
         }
         flag += 100
         search = GoogleSearch(params)
         results = search.get_dict()
         if "articles" in results:
            articles_num += len(results["articles"])
         results["articles_num"] = articles_num
    return results 
    




def home_views(request):
   labos = Equipe.objects.all()
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




def Profil_views(request):
    chercheur1 = Researcher.objects.get(id = request.user.pk)
    # pour recuperer les donnes
    chercheur = Researcher.objects.filter(id =request.user.pk)
    equipe = Equipe.objects.filter(id = chercheur[0].equipe_researchers.id)
    division = Division.objects.filter(id = equipe[0].division.id)
    etablisment = Etablisment.objects.filter(id =division[0].etablisment.id)
    apiData = ApiData(request.user.pk)
    if apiData == {}:
        context={'chercheur1':chercheur1,
                 'apiData':apiData,
                 'etablisment':etablisment,
                 'division':division,
                 'equipe':equipe}
    else:    
       inter =apiData["cited_by"]["graph"]
       max =0
       best_annee = 0
       for i in inter :
            if max < i["citations"]:
               max = i["citations"]
               best_annee =i["year"]
       context ={'best_annee':best_annee,
                 'chercheur1':chercheur1,
                 'apiData':apiData,
                 'etablisment':etablisment,
                 'division':division,
                 'equipe':equipe}
    return render (request,'profil.html',context)

def Profil_views_externe(request,pk):
    chercheur1 = Researcher.objects.get(id = pk)
    # pour recuperer les donnes
    chercheur = Researcher.objects.filter(id =pk)
    equipe = Equipe.objects.filter(id = chercheur[0].equipe_researchers.id)
    division = Division.objects.filter(id = equipe[0].division.id)
    etablisment = Etablisment.objects.filter(id =division[0].etablisment.id)
    apiData = ApiData(pk)
    if apiData == {'error': 'Your searches for the month are exhausted. You can upgrade plans on SerpApi.com website.'}:
        context ={'chercheur1':chercheur1,
                  'etablisment':etablisment,
                  'equipe':equipe,
                  'division':division,
                  'equipe':equipe}
    else:    
       inter =apiData
       max =0
       best_annee = 0
       for i in inter :
            if max < i["citations"]:
               max = i["citations"]
               best_annee =i["year"]
       context ={'best_annee':best_annee,'apiData':apiData,'chercheur1':chercheur1,'etablisment':etablisment,'equipe':equipe,'division':division,'equipe':equipe}
    return render (request,'profilE.html',context)





def Recup_id_equipe(request):
    i = Researcher.objects.get(pk = request.user.id)
    equipe_id = Equipe.objects.get(pk = i.equipe_researchers.id)
    context ={
       'equipe_id':equipe_id,
    } 
    return context

    



# affichage des listes de chercheur

def Liste_cher_Eta_aff(request):
    inter=Recup_id_etablisment(request)
    liste = CherList_eta(inter["etablisment_id"])
    info_etablisment = Etablisment.objects.get(pk = inter["etablisment_id"].id)
    context ={'liste':liste}
    context["info_etablisment"] = info_etablisment
    return render (request,'list_ch_eta.html',context)

def Liste_cher_Eta_aff_list(request):
    inter=Recup_id_etablisment(request)
    liste = CherList_eta (inter["etablisment_id"])
    info_etablisment = Etablisment.objects.get(pk = inter["etablisment_id"].id)
    context ={'liste':liste}
    context["info_etablisment"] = info_etablisment
    return render (request,'list_ch_eta-list.html',context)

        

def Liste_cher_Div_aff(request):
    inter=Recup_id_division(request)
    info_division = Division.objects.get(pk = inter["division_id"].id)
    liste = CherList_div (inter["division_id"])
    context ={'liste':liste}
    context["info_division"] = info_division
    return render (request,'list_ch_div.html',context)

def Liste_cher_Div_aff_list(request):
    inter=Recup_id_division(request)
    liste = CherList_div (inter["division_id"])
    info_division = Division.objects.get(pk = inter["division_id"].id)
    context ={'liste':liste}
    context["info_division"] = info_division
    return render (request,'list_ch_div-list.html',context)


def Liste_equipe_Eta_aff_list(request):
    inter=Recup_id_etablisment(request)
    liste = EquipeList_Eta(inter["etablisment_id"].id)
    info_etablisment = Etablisment.objects.get(pk = inter["etablisment_id"].id)
    context ={'liste':liste}
    context["info_etablisment"] = info_etablisment
    return render (request,'list_equipe_Eta.html',context)

def Liste_equipe_Div_aff_list(request):
    inter=Recup_id_division(request)
    liste = EquipeList_Div(inter["division_id"].id)
    info_division= Division.objects.get(pk = inter["division_id"].id)
    context ={'liste':liste}
    context["info_division"] = info_division
    return render (request,'list_equipe_Div.html',context)







def Liste_cher_Equipe_aff(request):
    inter=Recup_id_equipe(request)
    liste = CherList_equipe (request,inter["equipe_id"])
    info_equipe = Equipe.objects.get(pk = inter["equipe_id"].id)
    context ={'liste':liste}
    context["info_equipe"] = info_equipe
    return render (request,'list_ch_equipe.html',context)

def Liste_cher_Equipe_aff_list(request):
    inter=Recup_id_equipe(request)
    liste = CherList_equipe (request,inter["equipe_id"])
    info_equipe = Equipe.objects.get(pk = inter["equipe_id"].id)
    context ={'liste':liste}
    context["info_equipe"] = info_equipe
    return render (request,'list_ch_equipe-list.html',context)
# les affichage d'une chef de labo
  #DashLabo

  #Liste Equipe labo
def Liste_equipe_Div_aff (request):
    inter = Recup_id_division(request)
    inter2 = inter["division_id"]
    liste = EquipeList_Div(request,inter2)
    context ={'liste':liste}
    return render (request,'.html',context)
   #Liste Equipe labo 
      
      
      
# Les Fonction de test des role 
# test chef lab
def TestChefEquipe(reqeust):
   inter=Recup_id_equipe(reqeust)
   equipe = Equipe.objects.filter(id = inter["equipe_id"].id)
   if equipe[0].chef_equipe.id == reqeust.user.id:
       return True
   return False
    
# test chef lab habbes le3abe 
def TestChefDivision(reqeust):
   inter=Recup_id_division(reqeust)
   inter2 = inter["division_id"]
   equipe = Division.objects.filter(id = inter2)
   if equipe.chef_div.id == reqeust.user.id:
       return True
   return False 



def TestChefDivsion(reqeust):
   inter=Recup_id_etablisment(reqeust)
   inter2 = inter["etablisment_id"]
   equipe = Etablisment.objects.filter(id = inter2)
   if equipe.chef_etablisement.id == reqeust.user.id:
       return True
   return False  
def creat_equipe_views(request):
    OrderFormSet = inlineformset_factory(Division,Equipe,fields=('nom','site_web','chef_equipe'),extra = 1)
    inter = Recup_id_division(request)
    div = Division.objects.get(pk = inter["division_id"].id)
    form = OrderFormSet(queryset=Equipe.objects.none(),instance=div)
    if request.method =="POST":   
        form= OrderFormSet(request.POST, instance=div)
        if form.is_valid() :
             form.save()
             messages.success(request, 'Equipe a été ajouté avec succée')
             return redirect("createquipe")
         
    context={"form":form}
    return render(request,"createquipe.html",context)
    

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
    Etu=Equipe.objects.get(id=pk)
    Etu.delete()
    return redirect('G_chercheurs')

def EquipeList(): 
    i = Equipe.objects.all()
    return i


def EquipeList_Eta(pk):
    inter = Division.objects.filter(etablisment = pk)
    researchers = Equipe.objects.none()
    i =[]
    for i1 in inter:
       researchers = Equipe.objects.filter(division = i1.id)
       i +=researchers
    return i

#Les equipe d'un Divison
def EquipeList_Div(pk):#pk d'un labo
    i = Equipe.objects.filter(division = pk)
    return i

def Dash_Equipe_calc(pk):# on fait sous form de fonction pour utulistaion direct dans les autre dash board
    
    info_equipe = Equipe.objects.get(pk = pk)
    researchers = Researcher.objects.filter(equipe_researchers = pk) # recupere les chercheur des equipe
    nbr_cher_equipe = researchers.count()
    nbr_Citation = 0
    moy_indice_h = 0.0
    moy_indice_i10 = 0.0
    for i in researchers:
        inter = ApiData(i.id)
        if inter !={}:
           nbr_Citation += inter["cited_by"]["table"][0]["citations"]["all"]
           moy_indice_h += inter["cited_by"]["table"][1]["h_index"]["all"]  
           moy_indice_i10 += inter["cited_by"]["table"][2]["i10_index"]["all"]
    if nbr_cher_equipe == 0:
         moy_indice_hs = 0.0
         moy_indice_i10s = 0.0  
    else:  
       moy_indice_h = moy_indice_h/nbr_cher_equipe
       moy_indice_i10 = moy_indice_i10/nbr_cher_equipe
      
    context ={'nbr_cher_equipe':nbr_cher_equipe ,'info_equipe': info_equipe,'nbr_Citation':nbr_Citation,'moy_indice_h':moy_indice_h,'moy_indice_i10':moy_indice_i10}
    return context
    

def Dash_Equipe(request,pk):
    context = Dash_Equipe_calc(pk)
    return render (request,'DashEquipe.html',context)

def creat_division_views(request):
    OrderFormSet = inlineformset_factory(Etablisment,Division,fields=('nom','site_web','chef_div'),extra = 1)
    inter = Recup_id_etablisment(request)
    eta = Etablisment.objects.get(pk = inter["etablisment_id"].id)
    form = OrderFormSet(queryset=Division.objects.none(),instance=eta)
    if request.method =="POST":
        form= OrderFormSet(request.POST, instance=eta)   
        if form.is_valid() :
             form.save()
             messages.success(request, 'Division a été ajouté avec succée')
             return redirect("creatdiv")
        else:
            form =OrderFormSet(data=request.POST) 
            messages.success(request, 'Echec l\'hors de la creation !!')
    context={"form":form}
    return render(request,"creatdivision.html",context)


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

def Delete_division_views (request,pk):
    Etu=Division.objects.get(id =pk)
    Etu.delete()
    return redirect('G_chercheurs') 

def DivisionList_all(): 
    i = Division.objects.all()
    return i

def DivsionList_Eta(pk):
    i = Division.objects.filter(etablisment = pk)
    return i

def Recup_id_division(request):
    i = Researcher.objects.get(pk = request.user.id)
    equipe_id = Equipe.objects.get(pk = i.equipe_researchers.id)
    division_id = Division.objects.get(id = equipe_id.division.id)
    context ={
       'division_id':division_id,
    } 
    return context

def Liste_division_Eta_aff_list(request):
    inter=Recup_id_etablisment(request)
    liste = DivsionList_Eta(inter["etablisment_id"].id)
    info_etablisment = Etablisment.objects.get(pk = inter["etablisment_id"].id)
    context ={'liste':liste}
    context["info_etablisment"] = info_etablisment
    return render (request,'list_division_Eta.html',context)

def Dash_Division(request,pk):
    context = Dash_Division_calc(pk)
    return render (request,'DashDivision.html',context)

def Dash_Division_calc(pk):
     info_division = Division.objects.get(pk = pk)
     equipes = Equipe.objects.filter(division = pk)
     nbr_equipe_division = equipes.count()
     nbr_CitationL = 0
     nbr_cher_division=0
     moy_indice_hL = 0.0
     moy_indice_i10L = 0.0
     for i in equipes:
         inter = Dash_Equipe_calc(i.id)
         if inter !={}:
            nbr_CitationL += inter["nbr_Citation"]       
            moy_indice_hL += inter["moy_indice_h"]
            moy_indice_i10L += inter["moy_indice_i10"]
            nbr_cher_division += inter["nbr_cher_equipe"]
     if  nbr_equipe_division == 0:
         moy_indice_hL = 0.0
         moy_indice_i10L = 0.0  
     else: 
         moy_indice_hL=round(moy_indice_hL/nbr_equipe_division , 2)
         moy_indice_i10L=round(moy_indice_i10L/nbr_equipe_division, 2)
         
     
     context ={'nbr_equipe_division':nbr_equipe_division,
               'nbr_cher_division':nbr_cher_division ,
               'info_division': info_division,
               'nbr_Citation':nbr_CitationL,
               'moy_indice_h':moy_indice_hL,
               'moy_indice_i10':moy_indice_i10L}
     return context
 
 
def Dash_Division(request,pk):
    context = Dash_Division_calc(pk)
    return render (request,'DashDivision.html',context)




def Register_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    # wilaya = Location.objects.all()
    # etablisment= Etablisment.objects.all()
    # division= Division.objects.all()
    # laboratoire= Laboratoire.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            user1 = form.cleaned_data.get('last_name')
            messages.success(request,'Compte cree pour '+user +' '+user1)
            return redirect('login')
        # messages.error(request,'Verifier les inforamation fournit ')      
    context = {'form':form}              
            #    'etablisment':etablisment,
            #    'wilaya':wilaya,
            #    'laboratoire':laboratoire ,
            #    'division':division}

    return render (request,'register.html',context)

def Logout_views(request):
    logout(request)
    return redirect('login')
 
def Login_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    if request.method == 'POST':
        email =request.POST.get('email')
        password = request.POST.get('password')
        
        user =authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('profil')
        else:
            messages.info(request,'Email ou Mot de passe incorect')
    context = {}
    return render (request,'login.html',context)

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
       
def Delete_Etablisment_views (request,pk):
    Etu=Etablisment.objects.get(id=pk)
    Etu.delete()
    return redirect('home')       

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


def EtablismentList():
    i = Etablisment.objects.all()
    return i


def EtablismentList_location(pk):
    i = Etablisment.objects.filter(location = pk)
    return i

def Recup_id_etablisment(request):
    i = Researcher.objects.get(pk = request.user.id)
    equipe_id = Equipe.objects.get(pk = i.equipe_researchers.id)
    division_id = Division.objects.get(id = equipe_id.division.id)
    etablisment_id = Etablisment.objects.get(id = division_id.etablisment.id)
    context ={
       'etablisment_id':etablisment_id 
    } 
    return context


def Dash_Eta_calc(pk):
     info_etablisment = Etablisment.objects.get(pk = pk)
     divisions = Division.objects.filter(etablisment = pk )
     nbr_division_etablisment = divisions.count()
     nbr_equipe_etablisment=0
     nbr_CitationL = 0
     nbr_cher_etablisment=0
     moy_indice_hL = 0.0
     moy_indice_i10L = 0.0
     for i in divisions:
         inter = Dash_Division_calc(i.id)
         if inter !={}:
            nbr_equipe_etablisment += inter["nbr_equipe_division"]
            nbr_CitationL += inter["nbr_Citation"]       
            moy_indice_hL += inter["moy_indice_h"]
            moy_indice_i10L += inter["moy_indice_i10"]
            nbr_cher_etablisment += inter["nbr_cher_division"]
     if  nbr_division_etablisment == 0:
         moy_indice_hL = 0.0
         moy_indice_i10L = 0.0  
     else: 
         moy_indice_hL=round(moy_indice_hL/nbr_division_etablisment , 2)
         moy_indice_i10L=round(moy_indice_i10L/nbr_division_etablisment,2)    
     context ={'nbr_equipe_etablisment':nbr_equipe_etablisment,
               'nbr_cher_etablisment':nbr_cher_etablisment ,
               'info_etablisment': info_etablisment,
               'nbr_division_etablisment':nbr_division_etablisment,
               'nbr_Citation':nbr_CitationL,
               'moy_indice_h':moy_indice_hL,
               'moy_indice_i10':moy_indice_i10L}
     return context
 
def Dash_Etablisemnt(request,pk):
    context = Dash_Eta_calc(pk)
    return render (request,'DashEtablisment.html',context)


def Delete_Cher_views (request,pk):
    Etu=Researcher.objects.get(id = pk)
    Etu.delete()
    return redirect('G_chercheurs')


def CherList_equipe(pk):# pk represent l'id de l'equipe (rest a test)
    researchers = Researcher.objects.filter(equipe_researchers = pk)
    return researchers

def CherList_div(pk):
    inter = Equipe.objects.filter(division = pk)
    researchers = Researcher.objects.none()
    inter2 =[]
    for i in inter:
       researchers = Researcher.objects.filter(equipe_researchers = i.id)
       inter2 +=researchers
    return inter2

def CherList_eta(pk):
     inter = Division.objects.filter(etablisment = pk)
     interEquipe = Equipe.objects.none()
     inter2 =[]
     for i in inter:
        interEquipe = Equipe.objects.filter(division = i.id)
        inter2 +=interEquipe 
     final =[]
     for i in inter2:
        researchers = Researcher.objects.filter(equipe_researchers = i.id)
        final +=researchers
     return final