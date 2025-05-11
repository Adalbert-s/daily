# serializers.py
from rest_framework import serializers
from .models import TodoNota, User  # ou Note, conforme o seu nome

class TodoNotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoNota
        fields = ['id', 'titulo', 'descricao', 'data', 'hora']

def create(self, validated_data):
    user_id = validated_data.pop('user')
    user = User.objects.get(pk=user_id)
    return TodoNota.objects.create(user=user, **validated_data)

