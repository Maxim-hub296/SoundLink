import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

User = get_user_model()


class JWTAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )

    def _get_tokens(self):
        response = self.client.post(
            "/api/auth/login/", json.dumps(
                {
                    "username": "testuser",
                    "password": "test123"
                }
            ),
            content_type="application/json",
        )
        return response.json()

    def test_login(self):
        response = self.client.post(
            "/api/auth/login/", json.dumps(
                {
                    "username": "testuser",
                    "password": "test123"
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    def test_register(self):
        response = self.client.post(
            "/api/auth/register/", json.dumps(
                {
                    "username": "testuser1",
                    "password": "test1234",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    def test_logout_with_refresh_token(self):
        tokens = self._get_tokens()
        response = self.client.post(
            "/api/auth/logout/", json.dumps(
                {
                    "refresh": tokens["refresh"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("success", data)

    def test_logout_with_invalid_refresh_token(self):
        response = self.client.post(
            "/api/auth/logout/", json.dumps(
                {
                    "refresh": "hfhdhhdh13",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)

    def test_get_token_refresh(self):
        tokens = self._get_tokens()
        response = self.client.post(
            "/api/auth/refresh/", json.dumps(
                {
                    "refresh": tokens["refresh"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
