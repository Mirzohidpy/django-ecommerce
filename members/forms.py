from django import forms
from .models import Member


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['email', 'first_name', 'last_name', 'password']
