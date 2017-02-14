from django import forms
from .models import Game, Category


class GameUploadForm(forms.ModelForm):
    game_category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Game
        fields = ('name', 'description', 'logo', 'resource_info', 'game_category', 'cost')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
        labels = {
            'logo': ('Game Logo'),
            'resource_info': ('Resource URL'),
            'cost': ('Cost'),
        }
