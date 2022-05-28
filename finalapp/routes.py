from django.urls import path, include
from finalapp._views.charts import *
from finalapp._views.equipe import *
from finalapp._views.authentication import Login_views
from finalapp._views.user_profle import *

urlpatterns = [
    path('try/', try_view, name="try"),
    path('user/profile/', user_profile, name='profile'),
    path('equipe/<int:pk>/', Dash_Equipe),
    path('auth/', include([
        path('login/', Login_views, name="login"),
        # path('register/', register_view , name="register"),
        # path('logout/', logout_view , name="logout")
    ])),
    path('equipe/chercheur', Liste_cher_Equipe_aff_list),
    path('equipe/membre/', Profil_views_externe, {'pk': id}),
    # path('equipe/dash', )
    # path('user/division/create',)

]
