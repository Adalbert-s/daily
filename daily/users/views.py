from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático do usuário
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard_home')  # ou para a página que preferir
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Cadastro'})
