from django import forms
from django.contrib.auth.models import User
from gamestoredata.models import UserProfile, Game
from gamestoredata.constants import USER_CHOICES


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'user_type')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        labels = {
            'website': ('Personal website (optional)'),
            'picture': ('Upload Profile Picture (optional)'),
        }


class GameUploadForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'description', 'logo', 'resource_info', 'cost')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
