from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Rota para o dashboard
    path('getNotas/', views.get_notes, name='getNotas'),
    path('createNota/', views.create_note, name='createNota'),
    path('updateNota/<int:note_id>/', views.update_note, name='updateNota'),
    path('deleteNota/<int:note_id>/', views.delete_note, name='deleteNota'),
    
    path('check/', views.check_upcoming_notes, name='checkNotes'),
    path('gerar-relatorio/', views.gerar_relatorio, name='gerar_relatorio'),

]
