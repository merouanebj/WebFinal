from django.urls import path, include
from finalapp._views.charts import *
from finalapp._views.equipe import *
from finalapp._views.authentication import Login_views
from finalapp._views.user_profle import Profil_views

urlpatterns = [
    path('try/', try_view, name="try"),
    path('profile/', Profil_views, name='profile'),
    path('equipe/<int:pk>/', Dash_Equipe),
    path('auth/login/', Login_views, name="login"),
    # path('user/division/create',)
]
