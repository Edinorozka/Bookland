"""
Definition of forms.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog
from .models import Reviews
from .models import User

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'placeholder':'Password'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        labels = {
                'email': 'E-mail'
            }

class AnketaForm(forms.Form):
    name = forms.CharField(label = 'Ваше имя', max_length = 100)
    gender = forms.ChoiceField(label = 'Ваш пол',
                               choices = [('1', 'Мужской'), ('2', 'Женский')],
                               widget = forms.RadioSelect, initial = 1)
    age = forms.IntegerField(label = 'Ваш возраст', min_value = 1, max_value = 150)
    about = forms.ChoiceField(label = 'Вы хотите рассказать о книге или о сайте',
                              choices = [('1', 'О книге'), ('2', 'О сайте')],
                              widget = forms.RadioSelect, initial = 1)
    text = forms.CharField(label = 'Расскажите ваше мнение', widget = forms.Textarea(attrs = {'rows':5, 'cols':40}))
    email = forms.EmailField(label = 'Ваш e-mail')

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': 'Краткое описание', 'content': "Полный текст", 'image': "Картинка"}

class SearchForm(forms.Form):
    query = forms.CharField(label = "Поиск", required=False)

class ReviewsForm (forms.ModelForm):
    grade = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], label='Оценка')
    class Meta:
        model = Reviews
        fields = ('text', 'grade')
        labels = {'text': "Отзыв", 'grade': "Оценка"}
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
        }

class ChangeUserForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address')
        labels = {'first_name': "Имя", 'last_name': "Фамилия", 'address': "Адрес"}

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ProcessOrderForm(forms.Form):
    username = forms.CharField(label = 'Имя пользователя', max_length = 100)
    email = forms.CharField(label = 'Почта', max_length = 100)
    address = forms.CharField(label = 'Адресс', max_length = 100)
    card_number = forms.CharField(label = 'Номер карты', max_length = 100)