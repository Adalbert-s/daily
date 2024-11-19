from django.urls import path
from . import views
from .views import create_note, get_notes

urlpatterns = [  
    path('', views.home, name='dashboard_home'),
    path('api/notes/', views.get_notes, name='get_notes'),  # GET para listar as notas
    path('api/notes/create/', views.create_note, name='create_note'),  # POST para criar uma nova nota
    path('api/notes/<int:note_id>/update/', views.update_note, name='update_note'),  # PUT para atualizar nota
    path('api/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),  # DELETE para excluir nota
]

