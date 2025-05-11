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
def create_note(request):
    """Cria uma nova nota sem exigir autenticacao"""
    try:
        user_id = request.data.get('user')
        user = User.objects.get(pk=user_id) if user_id else None

        serializer = NoteSerializer(
            data={
                'titulo': request.data.get('titulo', ''),
                'descricao': request.data.get('descricao', ''),
                'data': request.data.get('data', ''),
                'hora': request.data.get('hora', ''),
                'user': user.id if user else None
            },
            context={'request': request}
        )

        if serializer.is_valid():
            note = serializer.save()
            return Response(serializer.data, status=201)

        return Response({'errors': serializer.errors}, status=400)

    except User.DoesNotExist:
        return Response({'error': 'Usuario nao encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao criar nota: {str(e)}")
        return Response({'error': str(e)}, status=500)
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
