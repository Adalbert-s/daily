# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Aqui você pode adicionar campos personalizados, se precisar
    pass
