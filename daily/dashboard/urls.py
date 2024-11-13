from django.urls import path
from . import views

urlpatterns = [  
    path('', views.home, name='dashboard_home'),
    path('api/notes/', views.get_notes, name='get_notes'),
    path('api/notes/create/', views.create_note, name='create_note'),
    path('api/notes/<int:note_id>/update/', views.update_note, name='update_note'),
    path('api/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]

