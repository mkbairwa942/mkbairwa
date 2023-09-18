
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password')
    
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'style': 'width: 100%',
        'placeholder':'Enter your name'
    }))

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name','username','password1','password2')
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'width: 100%',
        'placeholder':'Enter your name'
    }))

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'style': 'width: 100%',
        'placeholder':'Enter your Email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'style': 'width: 100%',
        'class':'password',
        'placeholder':'Enter your password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'style': 'width: 100%',
        'class':'password',
        'placeholder':'Confirm your password'
    }))