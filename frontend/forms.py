from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.CharField(label="Email", max_length=255)
    password1 = forms.CharField(label="Password", max_length=100)
    password2 = forms.CharField(label="Password", max_length=100)
