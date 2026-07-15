import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SongTestCase(TestCase):
    def setUp(self):
        self.media_dir = tempfile.mkdtemp()
        self._override = override_settings(MEDIA_ROOT=self.media_dir)
        self._override.enable()

        self.user = User.objects.create_user(
            username="test", password="test123"
        )
        self.client = APIClient()
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def tearDown(self):
        self._override.disable()
        shutil.rmtree(self.media_dir, ignore_errors=True)

    def _upload_song(self, filename="test.mp3", content=b'\xff\xfb\x90\x00' + b'\x00' * 413,
                     content_type="audio/mpeg", **extra):
        uploaded = SimpleUploadedFile(filename, content, content_type=content_type)
        data = {"file": uploaded, "title": "test", "artist": "artist", "length": 120}
        data.update(extra)
        return self.client.post("/api/songs/upload/", data)

    def test_upload_mp3_song(self):
        uploaded = SimpleUploadedFile("test.mp3", b'\xff\xfb\x90\x00' + b'\x00' * 413, content_type="audio/mpeg")

        response = self.client.post("/api/songs/upload/", {
            "file": uploaded,
            "title": "test",
            "artist": "test author",
            "length": 120,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_txt_file_rejected(self):
        uploaded = SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain")
        response = self.client.post("/api/songs/upload/", {
            "file": uploaded,
            "title": "test",
            "artist": "artist",
            "length": 120,
        })
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE])

    def test_upload_oversized_file_rejected(self):
        big_content = b'\xff\xfb\x90\x00' + b'\x00' * (21 * 1024 * 1024)
        uploaded = SimpleUploadedFile("big.mp3", big_content, content_type="audio/mpeg")
        response = self.client.post("/api/songs/upload/", {
            "file": uploaded,
            "title": "big",
            "artist": "artist",
            "length": 120,
        })
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE])

    def test_delete_song(self):
        upload_resp = self._upload_song()
        self.assertEqual(upload_resp.status_code, status.HTTP_201_CREATED)
        song_id = upload_resp.data["id"]

        response = self.client.delete("/api/songs/delete/", {"id": song_id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_songs(self):
        self._upload_song(filename="song1.mp3")
        self._upload_song(filename="song2.mp3")

        response = self.client.get("/api/songs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_one_song(self):
        id_song = self._upload_song(filename="song1.mp3").data["id"]
        response = self.client.get(f"/api/songs/{id_song}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
