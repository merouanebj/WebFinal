from django.urls import path
from finalapp.views import *

urlpatterns = [
    path('', home_views, name='landing'),
    
   #  path('createquipe/', creat_equipe_views, name="createquipe "),
    path('register/', Register_views, name="register"),
    path('login/', Login_views, name="login"),
    path('logout/', Logout_views, name="logout"),
    path('profil/', Profil_views, name='profil'),
    path('profil/membre/<int:pk>/', Profil_views_externe, name='profilE'),
    
    
    path('test/', Test, name='Test'),
    path('ListChercheurEta/', Liste_cher_Eta_aff, name='Liste_Ch_Eta'),
    path('ListChercheurDiv/', Liste_cher_Div_aff, name='Liste_Ch_Div'),
    
    
    
    # chef equipe
       #les chercheur de son equipe + dashboard
       path('DashEquipe/<int:pk>/', Dash_Equipe, name='Dash_equipe'),
       path('dashetablisment/<int:pk>/', Dash_Etablisemnt, name='Dash_etablisment'),
       
       path('ListChercheurEquipe/', Liste_cher_Equipe_aff, name='Liste_Ch_Equipe'),
       path('ListChercheurEquipe/liste/', Liste_cher_Equipe_aff_list, name='Liste_Ch_Equipe_liste'),
       
    # chef laboratoire
       # les chercheur du labo + dashLab + Les equipe   
     
      
      #  path('ListChercheurLab/chefequipe', Liste_cher_Lab_aff_chef_equipe, name='Liste_Ch_Lab'),
      #  path('ListEquipeLab/', Liste_equipe_Lab_aff, name='Liste_Equipe_Lab'),
       

    # chef Division
       #les chercheur de la division
         # path('dashdivision/<str:pk>/', Dash_Division, name='Dash_div'),
         path('ListChercheurDivision/', Liste_cher_Div_aff, name='Liste_Ch_Division'),
         path('ListChercheurDivision/liste/', Liste_cher_Div_aff_list, name='Liste_Ch_Division_liste'),
         path('ListEquipeDivision/liste/', Liste_equipe_Div_aff_list, name='Liste_equipe_Division_liste'),
         path('DashDivsion/<int:pk>/', Dash_Division, name='Dash_division'),
       
    #chef d'etablisment   
      #  path('creatdiv/', creat_division_views, name="creatdiv"),
       path('ListChercheurEtablisment/',       Liste_cher_Eta_aff, name='Liste_Ch_Etablisment'),
       path('ListChercheurEtablisment/liste/', Liste_cher_Eta_aff_list, name='Liste_Ch_Etablisment_liste'),
       path('ListEquipeEtablisment/liste/', Liste_equipe_Eta_aff_list, name='Liste_equipe_Etablisment_liste'),
      #  path('ListDivisionEtablisment/liste/', Liste_division_Eta_aff_list, name='Liste_division_Etablisment_liste'),
       
       
     #
    
         
     #delegue
       path('createta/', creat_Etablisment_views, name="createta"),
       
]  
