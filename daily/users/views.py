# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm  # Importe o formulário aqui

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário
            login(request, user)  # Faz login automático
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard_home')  # Redireciona para o dashboard
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Cadastro'})
