from django.contrib.auth.views import LoginView
from django.urls import path
from . import forms
from . import views

urlpatterns = [
    path('login/', 
         LoginView.as_view(
             template_name='users/login.html',
             authentication_form=forms.BootstrapAuthenticationForm
         ), 
         name='login'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
]
