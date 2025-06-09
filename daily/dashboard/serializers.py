# serializers.py
from rest_framework import serializers
from .models import TodoNota  # ou Note, conforme o seu nome

class TodoNotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoNota
        fields = ['id', 'titulo', 'descricao', 'data', 'hora', 'user']

    def create(self, validated_data):
        # Asegure-se de que o 'user' esteja associado ao usuÃ¡rio autenticado
        user = self.context['request'].user  # Pega o usuÃ¡rio autenticado
        note = TodoNota.objects.create(user=user, **validated_data)
        return note
