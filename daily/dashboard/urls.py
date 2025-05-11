from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Rota para o dashboard
    path('get-todonotas/', views.get_notes, name='get_todonotas'),
    path('create-todonota/', views.create_note, name='create_todonota'),
    path('update-todonota/<int:note_id>/', views.update_note, name='update_todonota'),
    path('delete-todonota/<int:note_id>/', views.delete_note, name='delete_todonota'),
    
]
