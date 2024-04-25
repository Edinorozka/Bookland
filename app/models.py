"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое описание")
    content = models.TextField(verbose_name = "Полный текст")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default ="background.jpg", verbose_name = "Путь к файлу")

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст коментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    post = models.ForeignKey(Blog, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Статья")

    def get_absolute_url(self):
        return reverse("comment", args=[str(self.post)])

    def __str__(self):
        return self.text

    class Meta:
        db_table = "comment"
        verbose_name = "коментарий статьи"
        verbose_name_plural = "коментарии статьи"

admin.site.register(Blog)
admin.site.register(Comment)
