from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Playlist

User = get_user_model()


# TODO: Дописать тесты доступности плейлиста (private, friend-only, public)
class PlaylistTestCase(TestCase):
    def setUp(self):
        self.api_route = "/api/playlists"
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = APIClient()
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_create_playlist(self):
        response = self.client.post(
            f"{self.api_route}/create/",
            {
                "title": "title_test",
                "description": "description_test",

            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(
            title="title_test",
            description="description_test",
            user=self.user,
        )
        response = self.client.delete(f"{self.api_route}/delete/{int(playlist.id)}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_empty_list_user_playlists(self):
        response = self.client.get(self.api_route + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_empy_list_user_playlists(self):
        playlist = Playlist.objects.create(
            title="title_test",
            description="description_test",
            user=self.user,
        )
        response = self.client.get(self.api_route + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
