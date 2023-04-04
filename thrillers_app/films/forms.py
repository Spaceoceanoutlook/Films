from captcha.fields import CaptchaField
from django import forms
from films.models import Film, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = [
            'title',
            'year',
            'genre',
            'country',
            'rating',
            'content',
            'photo',
            'recommendation',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text'
        ]


class UserRegForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль еще раз', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    captcha = CaptchaField()

