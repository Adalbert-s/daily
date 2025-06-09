from rest_framework import serializers
from .models import TodoNota


class TodoNotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoNota
        fields = ['id', 'titulo', 'descricao', 'data', 'hora', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']

    def create(self, validated_data):
        user = self.context['request'].user
        return TodoNota.objects.create(user=user, **validated_data)
