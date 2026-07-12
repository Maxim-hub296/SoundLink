from django.urls import path

from .views import SongUploadView, SongListView, SongDeleteView

app_name = "songs"
urlpatterns = [
    path("upload/", SongUploadView.as_view(), name="song-upload"),
    path("delete/", SongDeleteView.as_view(), name="song-delete"),
    path("/", SongListView.as_view(), name="song-list"),
]
