# users/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Adicione campos personalizados aqui, se necessário
    pass
