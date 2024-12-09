"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.CharField(max_length = 128, verbose_name = "Адресс", null=True)
    card_number = models.CharField(max_length = 128, verbose_name = "Номер карты", null=True)
    def get_absolute_url(self):
        return f'/changeUser/{self.id}'

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое описание")
    content = models.TextField(verbose_name = "Полный текст")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(verbose_name = "Путь к файлу")

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

class Books(models.Model):
    isbn = models.IntegerField(unique = True, verbose_name = "Isbn", primary_key = True)
    title = models.CharField(max_length = 100, verbose_name = "Заголовок")
    about = models.TextField(verbose_name = "Краткое описание")
    genre = models.CharField(max_length = 100, verbose_name = "Жанр книги")
    posted = models.DateTimeField(verbose_name = "Дата публикации")
    author = models.CharField(max_length = 256, verbose_name = "Автор")
    image = models.FileField(verbose_name = "Фото товара")
    prise = models.IntegerField(verbose_name = "Цена")
    number = models.IntegerField(verbose_name = "Количество на складе", default=0)

    def get_absolute_url(self):
        return reverse("book", args=[str(self.isbn)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Books"
        verbose_name = "товар"
        verbose_name_plural = "товары"

class Purchases(models.Model):
    cart = "cart"
    collect = "Собирем заказ"
    deliver = "Доставляем"
    delivered = "Доставленно"
    received = "Получено"
    CHOIS = [
        (cart, cart),
        (collect, 'Собирем заказ'),
        (deliver, 'Доставляем'),
        (delivered, 'Доставленно'),
        (received, 'Получено'),
        ]
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата заказа", null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Заказчик")
    status = models.CharField(max_length = 128, verbose_name = "статус заказа", null=True, choices = CHOIS)
    books = models.ManyToManyField(Books, through='Purchases_books')
    address = models.CharField(max_length = 128, verbose_name = "Адресс", null=True)

    def get_absolute_url(self):
        return reverse("purchases", args=[str(self.id)])

    class Meta:
        db_table = "Purchases"
        ordering = ["-date"]
        verbose_name = "заказ"
        verbose_name_plural = "покупки"

class Purchases_books(models.Model):
    purchases = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    number = models.IntegerField(default = 1)

class Reviews(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Заказчик")
    text = models.TextField(verbose_name = "отзыв")
    book = models.ForeignKey(Books, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Заказчик")
    grade = models.IntegerField()

    def get_absolute_url(self):
        return reverse("reviews", args=[str(self.id)])

    def __str__(self):
        return self.text

    class Meta:
        db_table = "Reviews"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

admin.site.register(Blog)
admin.site.register(Books)
admin.site.register(Comment)
admin.site.register(Reviews)
