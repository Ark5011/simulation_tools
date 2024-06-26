from django import forms
from .models import Formulation

class TgForm(forms.ModelForm):

    class Meta:
        model = Formulation
        fields = '__all__'

    