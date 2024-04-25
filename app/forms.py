"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

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