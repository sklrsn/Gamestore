from django import forms
from .models import Game


class GameUploadForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'description', 'logo', 'resource_info', 'cost')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
        labels = {
            'logo': ('Game Logo'),
            'resource_info': ('Resource URL'),
            'cost': ('Cost'),
        }
