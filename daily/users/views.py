
# Create your views here.

from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect(request.POST.get('next', 'dashboard_home'))  # Redirect to home after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationError(request, data=request.POST)
        if form.is_valid():
            user = _Authenticator(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next', 'dashboard'))   
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Log in'})