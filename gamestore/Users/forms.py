from django import forms
from django.contrib.auth.models import User
from common.constants import USER_CHOICES
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

"""
@Class_Name: UserForm
@Params: password
"""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


"""
@Class_Name: UserProfileForm
@Params: user_type - developer or player
"""


class UserProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'user_type')


"""
@Class_Name: USerProfileUpdateForm
@Params: model - user profile, website, picture (image)
"""


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        labels = {
            'website': ('Personal website (optional)'),
            'picture': ('Upload Profile Picture (optional)'),
        }


"""
@Class_Name: RegistrationForm
@Params: Username - name of the user
         email  - email address of the user
         password1 - password
         password2 - password ( matches the first password)
         user_type - developer/Player
"""


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=4, max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'abcd@email.com'}))
    password1 = forms.CharField(required=True, min_length=8, max_length=30, label="Password",
                                widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput())
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, label="Role")

    def clean(self):
        super(UserCreationForm, self).clean()

        if User.objects.filter(email=self.cleaned_data.get('email')).count() > 0:
            raise ValidationError("E-mail already registered")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
