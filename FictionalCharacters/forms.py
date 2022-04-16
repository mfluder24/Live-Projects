from django import forms
from django.forms import Textarea
from .models import Characters, Series

# Create a ModelForm
class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Characters
        fields = '__all__'
        widgets = {
            'notes': Textarea(attrs={'cols': 15, 'rows': 3}),
        }


