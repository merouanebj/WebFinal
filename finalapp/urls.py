
from django.urls import path
from finalapp.views import *
urlpatterns = [
    path('', home_views, name='landing'),
    
    path('createquipe/', creat_equipe_views, name="createquipe "),
    path('register/', Register_views, name="register"),
    path('login/', Login_views, name="login"),
    path('logout/', Logout_views, name="logout"),
    path('profil/', Profil_views, name='profil'),
    
    
    path('test/', Test, name='Test'),
    path('ListChercheurEta/', Liste_cher_Eta_aff, name='Liste_Ch_Eta'),
    path('ListChercheurDiv/', Liste_cher_Div_aff, name='Liste_Ch_Div'),
    
    
    
    # chef equipe
       #les chercheur de son equipe + dashboard
       path('DashEquipe/<int:pk>/', Dash_Equipe, name='Dash_equipe'),
       path('ListChercheurEquipe/', Liste_cher_Equipe_aff, name='Liste_Ch_Equipe'),
       
    # chef laboratoire
       # les chercheur du labo + dashLab + Les equipe   
       path('DashLaboratoire/<str:pk>/', Dash_Laboratoire, name='Dash_laboratoire'),
       path('ListChercheurLab/', Liste_cher_Lab_aff, name='Liste_Ch_Lab'),
       path('ListChercheurLab/chefequipe', Liste_cher_Lab_aff_chef_equipe, name='Liste_Ch_Lab'),
       path('ListEquipeLab/', Liste_equipe_Lab_aff, name='Liste_Equipe_Lab'),
       

    # chef Division
       #les chercheur de la division
       path('creatlabo/', creat_labo_views, name="creatlabo"),
       
    #chef d'etablisment   
       path('creatdiv/', creat_division_views, name="creatdiv"),
       
       
     #delegue
       path('createta/', creat_Etablisment_views, name="createta"),
       
]  
