from datetime import datetime
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import views
from users.forms import BootstrapAuthenticationForm
from dashboard import views as api_views  # Importando as views do app dashboard

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Login
    path('login/', 
         LoginView.as_view(
             template_name='users/login.html',
             authentication_form=BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),

    # Usuários
    path('users/', include('users.urls')),

    # Logout
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Admin
    path('admin/', admin.site.urls),

    # Dashboard (Aqui incluímos as URLs do app dashboard)
    path('dashboard/', include('dashboard.urls')),  # Certifique-se de que o app 'dashboard' tem um arquivo 'urls.py' e suas views


    # Registro
    path('register/', views.register, name='register'),
]
