from django.urls import path

from .views import SongUploadView, SongListView

urlpatterns = [
    path("songs/upload/", SongUploadView.as_view(), name="song-upload"),
    path("songs/", SongListView.as_view(), name="song-list"),
]
