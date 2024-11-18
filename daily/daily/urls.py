"""
Definition of urls for daily.
"""

from datetime import datetime
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import dashboard
from users.forms import BootstrapAuthenticationForm 
from app import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/',
         LoginView.as_view
         (
             template_name='users/login.html',
              authentication_form=BootstrapAuthenticationForm, 
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('users/', include('users.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('dashboard/', include("dashboard.urls")),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', include('users.urls')),
    path('register/', views.register, name='register'),
]
