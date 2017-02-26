from django import forms
from .models import Game, Category

"""
Class GameuploadForm
Fields: Name, Description, Logo, Resource Information, the category of the game and cost
"""


class GameUploadForm(forms.ModelForm):
    game_category = forms.ModelChoiceField(queryset=Category.objects.all(), initial="Select")

    class Meta:
        model = Game
        fields = ('name', 'description', 'logo', 'resource_info', 'game_category', 'cost')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
        labels = {
            'logo': ('Game Logo'),
            'resource_info': ('Game URL'),
            'cost': ('Amount'),
        }
