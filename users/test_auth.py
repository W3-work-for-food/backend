from django.test import TestCase
from django.core.cache import cache
from .models import User
from rest_framework.test import APIRequestFactory
from .auth import CustomAuthTokenSerializer


class CustomAuthTokenSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='testpassword')

    def tearDown(self) -> None:
        cache.clear()

    def test_validate(self):
        request = self.factory.post('/api-token-auth/', {'email': 'test@example.com', 'password': 'testpassword'})
        serializer = CustomAuthTokenSerializer(data=request.POST, context={'request': request})

        self.assertTrue(serializer.is_valid())

        # Test with wrong password
        request = self.factory.post('/api-token-auth/', {'email': 'test@example.com', 'password': 'wrongpassword'})
        serializer = CustomAuthTokenSerializer(data=request.POST, context={'request': request})

        self.assertFalse(serializer.is_valid())
