"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import ReviewsForm
from .models import Reviews
from .forms import BlogForm
from .forms import SearchForm
from .forms import RegisterUserForm
from .models import Books
from .models import User
from .forms import ChangeUserForm
from .forms import UserPasswordChangeForm
from .models import Purchases
from .forms import ProcessOrderForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data['query']
            if cd:
                cards = Books.objects.filter(models.Q(title__icontains = cd) | models.Q(author__icontains = cd) | models.Q(genre__icontains = cd))
                return render(
                    request,
                    'app/shops.html',
                    {
                        'title':'Магазин',
                        'form': form,
                        'cards': cards,
                        'year':datetime.now().year,
                    }
                )
    cards = Books.objects.all()
    if len(cards) > 0:
        return render(
            request,
            'app/shops.html',
            {
                'title':'Магазин',
                'form': form,
                'cards': cards,
                'year':datetime.now().year,
            }
        )
    else:
        return render(
            request,
            'app/shops.html',
            {
                'title':'Магазин',
                'form': form,
                'cards': '0',
                'year':datetime.now().year,
            }
        )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    if len(posts) > 0:
        return render(
            request,
            'app/blog.html',
            {
                'title':'Домашняя',
                'posts': posts,
                'year':datetime.now().year,
            }
        )
    else:
        return render(
            request,
            'app/blog.html',
            {
                'title':'Домашняя',
                'posts': '0',
                'year':datetime.now().year,
            }
        )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post.id)
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post': post,
            'year':datetime.now().year,
            'comments': comments,
            'form': form,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit = False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            return redirect('shop')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/NewPost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью',
            'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Наши контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'О компании',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    """Renders the Anketa page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2':'Жунщина'}
    about = {'1': 'О книге', '2':'О сайте'}

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['age'] = form.cleaned_data['age']
            data['about'] = about[form.cleaned_data['about']]
            data['text'] = form.cleaned_data['text']
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form = AnketaForm()
            
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        form = RegisterUserForm (request.POST)
        if form.is_valid(): #валидация полей формы
            user = form.save(commit=False)
            user.save()
            return redirect('login') # переадресация на главную страницу после регистрации
        else:
            messages.error(request, "Регистрация не удалась. Проверьте правильность заполнения формы")
            return redirect('registration')
    else:
        form = RegisterUserForm() # создание объекта формы для ввода данных нового пользователя
        return render(request, 'app/registration.html',
                      {
                       'form': form, # передача формы в шаблон веб-страницы
                       'year':datetime.now().year,
                      }
                     )

def product(request, parametr):
    """Renders the card page."""
    assert isinstance(request, HttpRequest)
    card = Books.objects.get(isbn=parametr)
    comments = Reviews.objects.filter(book=parametr)
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.book = Books.objects.get(isbn=parametr)
            comment_f.save()
            return redirect('product', parametr=card.isbn)
    else:
        form = ReviewsForm()
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    if len(cart) != 0:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books_through = cart.books.through.objects.filter(models.Q(books=card.isbn) & models.Q(purchases = cart))
        if len(books_through) > 0:
            books_through = cart.books.through.objects.get(models.Q(books=card.isbn) & models.Q(purchases = cart))
            return render(
                request,
                'app/product.html',
                {
                    'card': card,
                    'year':datetime.now().year,
                    'comments': comments,
                    'form': form,
                    'number': books_through
                }
            )
    return render(
        request,
        'app/product.html',
        {
            'card': card,
            'year':datetime.now().year,
            'comments': comments,
            'form': form,
            'number': 0
        }
    )

def purchases(request):
    """Renders the purchases page."""
    assert isinstance(request, HttpRequest)
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    books = 0
    books_through = {}
    message = 0
    if len(cart) != 0:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart')).books.all()
        if len(books) == 0:
            books = 0
        else:
            books_through = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart')).books.through.objects.filter(purchases = cart)
            for book in books_through:
                if book.number > books.get(isbn = book.books.isbn).number:
                    message = "Книги " + books.get(isbn = book.books.isbn).title + " нет в наличии в таком объёме"
    story = Purchases.objects.filter(user=request.user.id).exclude(status = 'cart')
    if len(story) == 0:
        story = 0
    return render(
            request,
            'app/purchases.html',
            {
                'cart': cart,
                'books': books,
                'carts': story,
                'number': books_through,
                'title':'заказы',
                'message': message,
                'year':datetime.now().year,
            }
        )   

def addbookView(request, parametr):
    """add book button."""
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    if len(cart) == 0:
        cart = Purchases.objects.create(user=request.user, status = 'cart')
        cart.books.add(parametr)
        cart.save()
    else:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books_through = cart.books.through.objects.filter(models.Q(books=parametr) & models.Q(purchases=cart))
        if len(books_through) > 0:
            books_through = cart.books.through.objects.get(models.Q(books=parametr) & models.Q(purchases=cart))
            card = Books.objects.get(isbn=parametr)
            if books_through.number != card.number:
                books_through.number = books_through.number + 1
                books_through.save()
        else:
            cart.books.add(parametr)
            cart.save()
    return redirect('product', parametr=parametr)

def downbookView(request, parametr):
    """down book button."""
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    if len(cart) > 0:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books_through = cart.books.through.objects.get(models.Q(books=parametr) & models.Q(purchases=cart))
        if books_through.number > 1:
            books_through.number = books_through.number - 1
            books_through.save()
        else:
            cart.books.remove(parametr)
            cart.save()
    return redirect('product', parametr=parametr)

def addbookView1(request, parametr):
    """add book button."""
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    if len(cart) == 0:
        cart = Purchases.objects.create(user=request.user, status = 'cart')
        cart.books.add(parametr)
        cart.save()
    else:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books_through = cart.books.through.objects.filter(models.Q(books=parametr) & models.Q(purchases=cart))
        if len(books_through) > 0:
            books_through = cart.books.through.objects.get(models.Q(books=parametr) & models.Q(purchases=cart))
            card = Books.objects.get(isbn=parametr)
            if books_through.number != card.number:
                books_through.number = books_through.number + 1
                books_through.save()
        else:
            cart.books.add(parametr)
            cart.save()
    return redirect('purchases')

def downbookView1(request, parametr):
    """down book button."""
    cart = Purchases.objects.filter(models.Q(user=request.user.id) & models.Q(status='cart'))
    if len(cart) > 0:
        cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
        books_through = cart.books.through.objects.get(models.Q(books=parametr) & models.Q(purchases=cart))
        if books_through.number > 1:
            books_through.number = books_through.number - 1
            books_through.save()
        else:
            cart.books.remove(parametr)
            cart.save()
    return redirect('purchases')

def deletebookView(request, parametr):
    """delete book button."""
    cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
    cart.books.remove(parametr)
    cart.save()
    return redirect('purchases')

class UpdateUser(UpdateView):
    model = User
    template_name = 'app/changeuser.html'

    form_class = ChangeUserForm

class buttonChangeClick(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("shop")
    template_name = "app/password_change_form.html"

def buttonDeleteUserClick(request):
    """Delet user button."""
    user = User.objects.get(id = request.user.id)
    user.delete()
    return redirect('shop')

def processOrderView(request):
    """Process an order form."""
    assert isinstance(request, HttpRequest)
    cart = Purchases.objects.get(models.Q(user=request.user.id) & models.Q(status='cart'))
    books = cart.books.through.objects.filter(purchases = cart)
    if request.method == 'POST':
        form = ProcessOrderForm(request.POST)
        if form.is_valid():
            cart.status = "Собирем заказ"
            cart.date = datetime.now()
            cart.address = form.cleaned_data['address']
            cart.save()
            #cards = Books.objects.filter(isbn = books.books)
            for book in books:
                card = Books.objects.get(isbn = book.books.isbn)
                card.number = card.number - cart.books.through.objects.get(models.Q(books = card.isbn) & models.Q(purchases=cart)).number
                card.save()
            return redirect('shop')
    else:
        form = ProcessOrderForm()
        form.initial = {'username': request.user.username,
                        'email': request.user.email,
                        'address': request.user.address,
                        'card_number': request.user.card_number}

    return render(
        request,
        'app/processOrder.html',
        {
            'form':form,
            'data':cart,
            'books': books
        }
    )