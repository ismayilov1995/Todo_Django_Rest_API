import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="İstifadəçi adı", required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label="Şifrə", required=True,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            return users.first().username.lower()
        return username.lower()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Şifrə və ya istifadəşi adı yanlışdır")


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label="İstifadəçi adı", required=True)
    password = forms.CharField(max_length=100, label="Şifrə", required=True, widget=forms.PasswordInput)
    password_check = forms.CharField(max_length=100, label="Şifrə təstiq", required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "password_check"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def clean_password_check(self):
        psw = self.cleaned_data.get('password')
        psw_check = self.cleaned_data.get('password_check')
        if psw and psw_check and (psw != psw_check):
            raise forms.ValidationError('Şifrələr eyni olmalıdır')
        return psw_check