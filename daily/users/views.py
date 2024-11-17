# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm  # Importe o formul�rio aqui

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usu�rio
            login(request, user)  # Faz login autom�tico
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard_home')  # Redireciona para o dashboard
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Cadastro'})
