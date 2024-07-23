from django import forms
from .models import Formulation

class TgForm(forms.ModelForm):

    class Meta:
        model = Formulation
        fields = ['water_min', 'casein', 'whey_protein', 'lactose', 'GOS', 'PDX'] 

    