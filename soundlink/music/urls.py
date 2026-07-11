from django.urls import path

from .views import SongUploadView, SongListView, SongDeleteView

urlpatterns = [
    path("songs/upload/", SongUploadView.as_view(), name="song-upload"),
    path("songs/delete/", SongDeleteView.as_view(), name="song-delete"),
    path("songs/", SongListView.as_view(), name="song-list"),
]
