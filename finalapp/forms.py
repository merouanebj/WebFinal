from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
                 'equipe_researchers'] 
              