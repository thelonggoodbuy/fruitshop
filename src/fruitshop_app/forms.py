from django import forms
# from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username_input', 'class': 'form-control me-2', 'type': 'text', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password_input', 'class': 'form-control me-2', 'type': 'password', 'placeholder': 'Password'}))


    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(LoginForm, self).__init__(*args, **kwargs)

    # def get_user(self):
    #     return self.user_cache