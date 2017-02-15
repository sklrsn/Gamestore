from django import forms
from GameArena.models import Game


"""
@Class_Name: CartForm
action can be "Add", "Remove"
Game
"""

class CartForm(forms.Form):
    action = forms.ChoiceField(choices=[('add','Add'), ('remove', 'Remove')], required=True)
    game = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.objects.all()
