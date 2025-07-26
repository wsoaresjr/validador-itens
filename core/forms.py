from django import forms
from .models import Validacao

class ValidacaoForm(forms.ModelForm):
    class Meta:
        model = Validacao
        fields = ['status']



# core/forms.py
from django import forms
from django.contrib.auth.models import Group

class UploadLoteForm(forms.Form):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
