from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache  # Import cache

User = get_user_model()

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        self.login_url = reverse("login")  # Adjust according to your login endpoint

    def get_token_for_user(self, user):
        """Generate JWT token for a given user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_token_generation_with_cache(self):
        """Verify token caching during login"""
        response = self.client.post(self.login_url, {"email": "testuser@example.com", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Validate token caching
        cached_token = cache.get(f'token:{self.user.email}')  # Ensure the cache key matches your implementation
        self.assertIsNotNone(cached_token)

    def test_permission_check(self):
        """Verify permission checks for accessing protected endpoints"""
        token = self.get_token_for_user(self.user)  # Generate token for the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)   

        # Protected view test
        response = self.client.get(reverse("protected_view"))  # Adjust for actual endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test without token
        self.client.credentials()  # Remove credentials
        response = self.client.get(reverse("protected_view"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
