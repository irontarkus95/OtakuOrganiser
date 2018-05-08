from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from urllib.request import urlopen, Request

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class RegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

    # def clean(self):
    #     userObj = self.cleaned_data
    #     username = userObj['username']
    #     email =  userObj['email']
    #     password =  userObj['password']
    #     if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
    #         User.objects.create_user(username, email, password)
    #         user = authenticate(username = username, password = password)
    #         login(request, user)
    #     else:
    #         raise forms.ValidationError('A username with that email or password already exists')
    #     return self.cleaned_data

    # def register(self, request):
    #     userObj = self.cleaned_data
    #     username = userObj['username']
    #     email =  userObj['email']
    #     password =  userObj['password']
    #     if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
    #         User.objects.create_user(username, email, password)
    #         user = authenticate(username = username, password = password)
    #         login(request, user)
    #     return user