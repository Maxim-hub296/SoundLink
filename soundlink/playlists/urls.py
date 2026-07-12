from django.urls import path

from .views import PlaylistCreateView, PlaylistsView, PlaylistDeleteView

app_name = "playlists"
urlpatterns = [
    path("create/", PlaylistCreateView.as_view(), name="playlist-create"),
    path("delete/", PlaylistDeleteView.as_view(), name="playlist-delete"),
    path("/", PlaylistsView.as_view(), name="playlists-list"),
]
