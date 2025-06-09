from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from .models import TodoNota as Note  # Renomeado para 'Note'
from .serializers import TodoNotaSerializer as NoteSerializer
from django.contrib.auth import get_user_model
import logging
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse

logger = logging.getLogger(__name__)
User = get_user_model()


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
        logger.error(f"Erro ao buscar notas: {str(e)}")
        return Response({'error': 'Erro ao buscar notas'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    """Cria uma nova nota associada ao usuario autenticado"""
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

        return Response({'errors': serializer.errors}, status=400)

    except Note.DoesNotExist:
        return Response({'error': 'Nota nao encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao atualizar nota: {str(e)}")
        return Response({'error': 'Erro interno do servidor'}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, pk):
    """Exclui uma nota existente"""
    try:
        note = Note.objects.get(pk=pk, user=request.user)
        note.delete()
        return Response({'message': 'Nota excluida com sucesso'}, status=204)

    except Note.DoesNotExist:
        return Response({'error': 'Nota nao encontrada'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao excluir nota: {str(e)}")
        return Response({'error': 'Erro interno do servidor'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_upcoming_notes(request):
    """Verifica se ha notas proximas do horario atual"""
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

        return Response(alertas, status=200)

    except Exception:
        return Response({'error': 'Erro ao verificar notas proximas'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gerar_relatorio(request):
    """Gera um relatorio em PDF com todas as notas do usuario"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, "Relatorio de Notas")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Usuario: {request.user.username}")
    p.drawString(50, height - 100, f"Email: {request.user.email}")

    notas = Note.objects.filter(user=request.user)

    if not notas:
        p.drawString(50, height - 140, "Nenhuma nota encontrada.")
    else:
        data = [["ID", "Titulo", "Descricao", "Data", "Hora", "Criado em"]]

        for nota in notas:
            data.append([
                str(nota.id),
                nota.titulo,
                nota.descricao,
                nota.data.strftime('%d/%m/%Y'),
                nota.hora.strftime('%H:%M'),
                nota.criado_em.strftime('%d/%m/%Y %H:%M')
            ])

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
