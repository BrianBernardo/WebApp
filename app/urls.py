from django.urls import path
from .views import HomePageView, AboutPageView, songPageView, songDetailsView, songCreateview, songUpdateView, songDeleteview

urlpatterns =[
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('song/', songPageView.as_view(), name='song'),
    path('song/<int:pk>', songDetailsView.as_view(), name='song_detail'),
    path('song/new', songCreateview.as_view(), name='new_song'),
    path('song/<int:pk>/edit', songUpdateView.as_view(), name='song_update'),
    path('song/<int:pk>/delete', songDeleteview.as_view(), name='song_delete'),
]