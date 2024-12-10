from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect


urlpatterns = [  
    path('', views.home, name='dashboard_home'),
    path('api/notes/', views.get_notes, name='get_notes'),
    path('api/notes/create/', views.create_note, name='create_note'),
    path('api/notes/<int:note_id>/update/', views.update_note, name='update_note'),
    path('api/notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('favicon.ico', lambda request: HttpResponseRedirect('https://icons.iconarchive.com/icons/paomedia/small-n-flat/256/notepad-icon.png')),
]

