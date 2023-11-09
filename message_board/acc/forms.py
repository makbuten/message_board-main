from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    nickname = forms.CharField(max_length=30, label='Псевдоним')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.nickname = self.cleaned_data['nickname']
        user.save()
        return user


class AccountForm(forms.ModelForm):
    nickname = forms.CharField(max_length=150, widget=forms.TextInput,
                               label='Псевдоним')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput,
                                 label='Имя', required=False)
    last_name = forms.CharField(max_length=150, widget=forms.TextInput,
                                label='Фамилия', required=False)

    class Meta:
        model = User
        fields = [
            'nickname',
            'first_name',
            'last_name',
        ]