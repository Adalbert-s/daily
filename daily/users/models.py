# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Aqui voc� pode adicionar campos personalizados, se precisar
    pass
