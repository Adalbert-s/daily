"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from django.contrib.auth import login
from django.http import HttpRequest
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import get_user_model



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def register(request):
    """Handles the user registration."""
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            # Processa o cadastro via API (JSON)
            try:
                import json
                data = json.loads(request.body.decode('utf-8'))
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')

                # Validação de campos obrigatórios
                if not username or not password:
                    return JsonResponse({'detail': 'Username e senha são obrigatórios.'}, status=400)

                # Criação do usuário
                user = get_user_model().objects.create_user(username=username, email=email, password=password)
                login(request, user)  # Loga o usuário automaticamente após o registro
                return JsonResponse({'detail': 'Cadastro realizado com sucesso!'}, status=200)
            except Exception as e:
                return JsonResponse({'detail': str(e)}, status=400)
        else:
            # Processa o cadastro via formulário tradicional
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  # Loga o usuário automaticamente após o registro
                return redirect('home')
            else:
                return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

