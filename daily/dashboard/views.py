from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .models import TodoNota as Note  # Renomeando TodoNota para Note
from .serializers import TodoNotaSerializer as NoteSerializer  # Renomeando TodoNotaSerializer para NoteSerializer
from django.contrib.auth import get_user_model
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes




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
# Adicionei o endpoint check_upcoming_notes para verificar notas proximas do horario
# e retornei uma lista de alertas com as notas que estao dentro do intervalo de 30 minutos.
# O endpoint retorna um status 200 OK com a lista de alertas ou um erro 500 se ocorrer algum problema.
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

#---------------------------------------------------------------------------------------------#

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gerar_relatorio(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Título
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, "Relatorio de Notas")

    # Informações do usuário
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Usuario: {request.user.username}")
    p.drawString(50, height - 100, f"Email: {request.user.email}")

    # Dados das notas
    notas = TodoNota.objects.filter(user=request.user)

    if not notas:
        p.drawString(50, height - 140, "Nenhuma nota encontrada.")
    else:
        data = [
            ["ID", "Titulo", "Descricao", "Data", "Hora", "Criado em"]
        ]

        for nota in notas:
            data.append([
                str(nota.id),
                nota.titulo,
                nota.descricao,
                nota.data.strftime('%d/%m/%Y'),
                nota.hora.strftime('%H:%M'),
                nota.criado_em.strftime('%d/%m/%Y %H:%M')
            ])

        # Tabela
        table = Table(data, colWidths=[2*cm, 4*cm, 6*cm, 2.5*cm, 2*cm, 4*cm])

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ])

        table.setStyle(style)

        table_width, table_height = table.wrap(0, 0)
        x = (width - table_width) / 2
        y = height - 160 - table_height

        table.drawOn(p, x, y)

    p.showPage()
    p.save()

    return response
