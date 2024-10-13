
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('dashboard')  # Redirect to home after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})

def dashboard_home(request):
    return render(request, 'dashboard/home.html', {'title': 'Dashboard'}) #