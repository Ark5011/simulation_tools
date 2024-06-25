from django import forms
from .models import Tg

class TgForm(forms.ModelForm):

    class Meta:
        model = Tg
        fields = '__all__'

    