from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from joatu.models import JoatuUser


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]


class JoatuUserForm(forms.ModelForm):

    class Meta:
        model = JoatuUser
        exclude = ['user',]
 

