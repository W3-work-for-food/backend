from django.test import TestCase
from django.core.cache import cache
from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='test1@example.com', password='test123')
        self.user2 = User.objects.create_user(username='user2', email='test2@example.com', password='test123')

    def tearDown(self) -> None:
        cache.clear()

    def test_user_inherits_abstractuser(self):
        # Check if User inherits from AbstractUser by checking an attribute unique to AbstractUser
        self.assertTrue(hasattr(self.user1, 'is_superuser'), "User model should inherit from AbstractUser")

    def test_user_unique_email(self):
        with self.assertRaises(Exception):
            # Attempt to create another user with the same email to test uniqueness
            User.objects.create_user(username='user3', email='test1@example.com', password='test123')

    def test_user_str_returns_username(self):
        self.assertEqual(str(self.user1), 'user1', "__str__ method should return the username")