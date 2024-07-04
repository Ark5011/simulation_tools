from django import forms
from .models import Gt_input

class Gtform(forms.ModelForm):

    class Meta:
        model = Gt_input
        fields = '__all__'

    