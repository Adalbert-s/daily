from django.db import models
from django.conf import settings  # Adiciona a importação de settings

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Atualiza para usar AUTH_USER_MODEL
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title
