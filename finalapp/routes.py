from django.urls import path, include
from finalapp._views.charts import *
from finalapp._views.equipe import *
from finalapp._views.authentication import Login_views
from finalapp._views.user_profle import *

urlpatterns = [
    path('try/', try_view, name="try"),
    path('equipe/<int:pk>/', Dash_Equipe),
    path('auth/', include([
        path('login/', Login_views, name="login"),
        # path('register/', register_view , name="register"),
        # path('logout/', logout_view , name="logout")
    ])),
    path('equipe/chercheur', Liste_cher_Equipe_aff_list),
    path('equipe/membre/', Profil_views_externe, {'pk': id}),

    # for a simple member
    path('u/profile/', user_profile, name='profile'),
    path('u/', include([
        path('equipe/members/', equipe_members,
             name='equipe_members'),  # only for chef_equipe ?
        path('equipe/dashboard/', equipe_dashboard,
             name='equipe_dashboard'),  # only for chef_equipe ?
        # path('equipe/add_member', equipe_add_member,),
        # path('equipe/delete_member', equipe_delete_member ),
        # path('equipe/change_name', change_equipe_name,)
    ])),
    # path('u/', include([
    # path('division/equipes', division_equipes , name='division_equipes'), # only for chef_division ?
    # path('division/dashboard', division_dashboard , name='division_dashboard'), # only for chef_division ?
    # path('division/add_equipe', division_add_equipe,),
    # path('division/delete_equipe', division_delete_equipe ),
    # path('division/change_name', change_division_name,),
    #
    # ]))
    # path('equipe/dash', )
    # path('user/division/create',)

]
