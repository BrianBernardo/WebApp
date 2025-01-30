from django.urls import path
from django.views.generic.base import RedirectView
from .views import HomePageView, AboutPageView, songPageView, songDetailsView, songCreateview, songUpdateView, songDeleteview, IndexPageView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/'), name='login_redirect'),
    path('home/', IndexPageView.as_view(), name='home'),  # You can keep this or change to 'main_page'
    path('mainpage/', HomePageView.as_view(), name='main_page'),  # This is the main page view
    path('about/', AboutPageView.as_view(), name='about'),
    path('song/', songPageView.as_view(), name='song'),
    path('song/<int:pk>', songDetailsView.as_view(), name='song_detail'),
    path('song/new', songCreateview.as_view(), name='new_song'),
    path('song/<int:pk>/edit', songUpdateView.as_view(), name='song_update'),
    path('song/<int:pk>/delete', songDeleteview.as_view(), name='song_delete'),
    path('playlists/', views.playlist_list, name='playlist_list'),  # List of user playlists
    path('playlists/create/', views.create_playlist, name='create_playlist'),  # Create a new playlist
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),  # View a specific playlist
    path('playlists/<int:playlist_id>/edit/', views.edit_playlist, name='edit_playlist'),  # Edit a playlist (add/remove songs)
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),  # Delete a playlist
]
