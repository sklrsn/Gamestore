from django import forms
from django.contrib.auth.models import User
from gamestoredata.models import UserProfile
from gamestoredata.usertypes import USER_CHOICES


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    usertype = forms.ChoiceField(choices=USER_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'usertype')
