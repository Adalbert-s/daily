from rest_framework import serializers
from .models import TodoNota
from django.contrib.auth import get_user_model

User = get_user_model()

class TodoNotaSerializer(serializers.ModelSerializer):
    # user pode ser read_only para evitar que o cliente envie
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TodoNota
        fields = ['id', 'titulo', 'descricao', 'data', 'hora', 'user']

    def create(self, validated_data):
        user = self.context['request'].user  # pega o user da requisição autenticada
        return TodoNota.objects.create(user=user, **validated_data)
