from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TodoNota(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data = models.DateField()   # Data da tarefa
    hora = models.TimeField()   # Hora da tarefa
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)      # Data e hora de criação
    atualizado_em = models.DateTimeField(auto_now=True)      # Data e hora da última atualização

    def __str__(self):
        return self.titulo
