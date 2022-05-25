from finalapp.views import *

from django.urls import path
urlpatterns = [
    path('', home_views, name='landing'),
    path('createquipe/', creat_equipe_views, name="createquipe"),
    path('register/', Register_views, name="register"),
    path('login/', Login_views, name="login"),
    path('logout/', Logout_views, name="logout"),
    path('profil/', Profil_views, name='profil'),

    path('user/<int:pk>/dashboard', user_personal_dash,
         name="dashboard_personal_de_user"),

    path('equipe/<int:pk>/dashboard',
         Dash_Equipe, name='Dash_equipe'),
    # path('user/<int:pk>/laboratoire/<str:pk>/dashboard',
    #      Dash_Laboratoire, name='Dash_laboratoire'),

    # path('user/<int:pk>/laboratoire/<str:pk>/equipes',
    #      lab_equipes, name='equipe lab'),

    # path('user/<int:pk>/laboratoire/<str:pk>/equipes/members',
    #      equipe_members, name='les membres d\'equipes'),

    # path('user/<int:pk>/division/<int:pk>/laboratoires',
    #      division_labs, name='les laboratoires de\'division <pk>'),
    # path('user/<int:pk>/division/<int:pk>/laboratoires/<str:pk>/equipes',
    #      equipe_members, name='les equipes de laboratoire'),

    # path('user/<int:pk>/division/<int:pk>/laboratoire/<str:pk>/equipes/members',
    #      equipe_members, name='les membres d\'equipes'),
]
