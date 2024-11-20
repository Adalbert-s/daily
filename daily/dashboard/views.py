from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

# View para renderizar a página inicial
def home(request):
    return render(request, 'dashboard/index.html')

# View para listar todas as notas do usuário autenticado (GET)
@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.filter(user=request.user)  # Filtra notas do usuário autenticado
    serializer = NoteSerializer(notes, many=True)
    logger.info(serializer.data)  # Log das notas retornadas
    return Response(serializer.data)

# View para criar uma nova nota (POST)
@permission_classes([IsAuthenticated])
@api_view(['POST'])

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_note(request):
    logger.info(f"Received request method: {request.method}")
    logger.info(f"Request data: {request.data}")
    
    # Copia os dados enviados e adiciona o usuário autenticado
    data = request.data.copy()
    data['user'] = request.user.id  # Adiciona o ID do usuário autenticado
    
    # Cria o serializer com os dados atualizados
    serializer = NoteSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()  # Salva no banco de dados
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para atualizar uma nota existente (PUT)
@api_view(['PUT'])
def update_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)  # Busca nota do usuário autenticado
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para deletar uma nota existente (DELETE)
@api_view(['DELETE'])
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)  # Busca nota do usuário autenticado
        note.delete()
        return Response({'message': 'Note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
