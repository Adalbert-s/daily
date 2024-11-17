from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Note  # ajuste conforme o nome do modelo
from .serializers import NoteSerializer

# Create your views here.
def home(request):
    return render(request, 'dashboard/index.html')

@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.all() 
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        note.delete()
        return Response({'message': 'Note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
