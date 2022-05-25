from dataclasses import field
from email import message
from pyexpat import model
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from serpapi import GoogleSearch
from django.contrib import messages


class EtablismentForm  (ModelForm):
      class Meta:
          model = Etablisment
          fields = '__all__'

class DivisionForm  (ModelForm):
      class Meta:
          model = Division
          fields = '__all__'          
          
class LaboratoireForm  (ModelForm):
      class Meta:
          model = Laboratoire
          fields = '__all__'        

class EquipeForm  (ModelForm):
      class Meta:
          model = Equipe
          fields = '__all__'
          
          
#Login Form      
class CreateUserForm(UserCreationForm):
    class Meta:
        model =Researcher
        fields =['first_name',
                 'last_name',
                 'email',
                 'speciality',
                 'grade',
                 'role',
                 'linkedin_account',
                 'google_scholar_account',
                 'equipe_researchers',
                 'password1',
                 'password2'] 
    def clean(self):
       cleaned_data = super().clean()   
       
       inter = self.cleaned_data.get('google_scholar_account')    
       if inter[0:26] != 'https://scholar.google.com':         
          raise forms.ValidationError(inter[0:25]+ ' format du compte google scholar  fournit non valide')
       inter = self.cleaned_data.get('google_scholar_account')
       params = {
       "engine": "google_scholar_author",
       "author_id":'FsN2xpQAAAAJ',
    #    "author_id": str(inter.partition("user=")[2][:12]),
       "api_key": "7e3cd1a6a37b960e426e2d09bcf5fec5ff3e62219a4bc1e42cd907b464e6977e"
       }
 
       search = GoogleSearch(params)
       results = str(search)
    #    if len(results) < 1000:
    #        raise forms.ValidationError(inter.partition("user=")[2][:12]+ ' Le compte google scholar n\'est pas valide , prier de le vérifier !')