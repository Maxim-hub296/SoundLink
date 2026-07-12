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
        self.client.login(username="testuser", password="test123")

    def test_get_token(self):
        response = self.client.post(
            "/auth/login/", json.dumps(
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
