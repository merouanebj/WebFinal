"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from finalapp.views import *
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_views, name='landing'),
    
    #Equipe
        path('createquipe/', creat_equipe_views ,name="createquipe"),
        path('register/', Register_views ,name="register"),
        path('login/', Login_views ,name="login"),
        path('logout/', Logout_views ,name="logout"),
        path('profil/' , Profil_views, name='profil'),
        path('DashEquipe/<int:pk>/' , Dash_Equipe, name='Dash_equipe'),
        path('DashLaboratoire/<str:pk>/' , Dash_Laboratoire, name='Dash_laboratoire'),
        path('test/' , Test, name='Test'),  
]
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()