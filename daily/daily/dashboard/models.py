from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class TodoNota(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data = models.CharField(max_length=10) 
    hora = models.CharField(max_length=5)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo