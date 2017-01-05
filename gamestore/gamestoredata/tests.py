from django.test import TestCase, client
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.c = client.Client()

    def test_profile_valid_url(self):
        response = self.client.get('/profile/login/')
        self.assertEqual(response.status_code, 200)

    def test_profile_invalid_url(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/profile/login')
        self.assertEqual(response.status_code, 301)

    def test_user_insert(self):
        user = User(email="abc@abc.com", password="abcdefgh123", username="abc");
        user.save();
        user = User.objects.get(email="abc@abc.com")
        self.assertEqual(user.username, 'abc')
