from django import forms
from .models import Gt

class Gtform(forms.ModelForm):

    class Meta:
        model = Gt
        fields = '__all__'

    