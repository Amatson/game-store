from django import forms
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from gamestore.models import Game


class SearchForm(forms.Form):
    category = forms.CharField(max_length=255, required=False)
    name = forms.CharField(max_length=255, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('username', 'password')


class RegisterForm(forms.Form):
    ACCOUNT_TYPE_CHOICES = (('player', 'Player'), ('developer', 'Developer'))

    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(max_length=255)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)

    class Meta:
        fields = ('username', 'password', 'first_name', 'last_name', 'account_type')


class GameForm(forms.Form):
    name = forms.CharField(max_length=255)
    category = forms.CharField(max_length=255)
    description = forms.CharField(max_length=500)
    game_url = forms.URLField()
    price = forms.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        fields = ('name', 'category', 'game_url', 'price', 'description')


class ScoreForm(forms.Form):
    score = forms.IntegerField()

    class Meta:
        fields = 'score'


class SaveForm(forms.Form):
    state = forms.CharField(max_length=10000)


class RequestLoadForm(forms.Form):
    request_load = forms.CharField(max_length=255)


class EditNameForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)


class EditPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(widget=forms.PasswordInput())


class EditGameForm(forms.Form):
    name = forms.CharField(max_length=255)
    category = forms.CharField(max_length=225)
    description = forms.CharField(max_length=500)
    price = forms.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        fields = ('name', 'category', 'price', 'description')
