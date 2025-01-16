from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

    def test_user_registration(self):
        """Test that a user can register successfully"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

    def test_user_login(self):
        """Test that a user can login and receive tokens"""
        # First create a user
        self.client.post(self.register_url, self.user_data)

        # Attempt to login
        login_data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        login_data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_registration(self):
        """Test registration with invalid data"""
        # Test with missing password
        invalid_data = self.user_data.copy()
        invalid_data.pop("password")
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
