from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .models import TodoNota as Note  # Renomeando TodoNota para Note
from .serializers import TodoNotaSerializer as NoteSerializer  # Renomeando TodoNotaSerializer para NoteSerializer
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    """Lista todas as notas do usuario autenticado"""
    try:
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching notes: {str(e)}")
        return Response(
            {'error': 'Failed to fetch notes'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, pk):
    """Atualiza uma nota existente"""
    try:
        note = Note.objects.get(pk=pk, user=request.user)
        serializer = NoteSerializer(note, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    except Note.DoesNotExist:
        return Response(
            {'error': 'Note not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error updating note: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, pk):
    """Exclui uma nota existente"""
    try:
        note = Note.objects.get(pk=pk, user=request.user)
        note.delete()
        return Response(
            {'message': 'Note deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
        
    except Note.DoesNotExist:
        return Response(
            {'error': 'Note not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting note: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
#---------------------------------------------------------------------------------------------#
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_upcoming_notes(request):
    """Verifica se ha notas proximas do horario"""
    try:
        now = datetime.now()
        alertas = []

        notes = Note.objects.filter(user=request.user)

        for note in notes:
            note_datetime = datetime.combine(note.data, note.hora)
            diff = note_datetime - now

            if timedelta(minutes=0) <= diff <= timedelta(minutes=30):
                alertas.append({
                    "id": note.id,
                    "titulo": note.titulo,
                    "descricao": note.descricao,
                    "data": note.data,
                    "hora": note.hora,
                    "mensagem": "Essa nota esta proxima do horario!"
                })

        return Response(alertas, status=status.HTTP_200_OK)

    except Exception:
        return Response(
            {'error': 'Erro ao verificar notas proximas.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
