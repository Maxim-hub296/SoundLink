from django.urls import path

from .views import PlaylistCreateView, PlaylistsView, PlaylistDeleteView

app_name = "playlists"
urlpatterns = [
    path("create/", PlaylistCreateView.as_view(), name="playlist-create"),
    path("delete/<int:pk>/", PlaylistDeleteView.as_view(), name="playlist-delete"),
    path("", PlaylistsView.as_view(), name="playlists-list"),
    path("<int:pk>/", PlaylistsView.as_view(), name="playlists-detail"),
]
