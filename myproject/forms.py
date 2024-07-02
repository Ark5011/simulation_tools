from django import forms
from tg_couchman.models import Project

class Projectform(forms.ModelForm):     
    class Meta:
        model = Project
        fields = '__all__'

    