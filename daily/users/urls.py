from django.contrib.auth.views import LoginView
from django.urls import path
from . import forms

urlpatterns = [
    path('login/', 
         LoginView.as_view(
             template_name='users/login.html',
             authentication_form=forms.BootstrapAuthenticationForm
         ), 
         name='login'),
]
