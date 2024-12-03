"""
Definition of urls for Bookland.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('product/<int:parametr>/', views.product, name='product'),
    path('purchases', views.purchases, name='purchases'),
    path('changeUser/<int:pk>/', views.UpdateUser.as_view(), name='changeUser'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('newpost/', views.newpost, name='newpost'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('processOrder/', views.processOrderView, name='processOrder'),

    path('changePassword/', views.buttonChangeClick.as_view(), name = 'changePassword'),
    path('deleteUser/', views.buttonDeleteUserClick, name='deleteUser'),
    path('addBook/<int:parametr>/', views.addbookView, name='addBook'),
    path('deleteBook/<int:parametr>/', views.deletebookView, name='deleteBook'),
    path('downbookView/<int:parametr>/', views.downbookView, name='downbookView'),
    path('addBook1/<int:parametr>/', views.addbookView1, name='addBook1'),
    path('downbookView1/<int:parametr>/', views.downbookView1, name='downbookView1'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()