from django import forms
from finalapp.models import Equipe


class CreateEquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
