from django.test import TestCase, client
from django.contrib.auth.models import User
from django.http import HttpRequest
from .views import update_profile
from .forms import UserProfileForm


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = client.Client()

    def test_valid_login_url(self):
        response = self.client.get('/profile/login/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_url(self):
        response = self.client.get('/profile/login')
        self.assertEqual(response.status_code, 301)

    def test_valid_change_password_url(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345678')
        user.save()
        self.client.login(username="testuser", password="12345678")
        response = self.client.get('/profile/change_password/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_change_password_url(self):
        response = self.client.get('/profile/change_password')
        self.assertEqual(response.status_code, 301)

    def test_valid_update_profile_url(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345678')
        user.save()
        logged_in = self.client.login(username="testuser", password="12345678")
        self.assertEqual(logged_in, True)
        response = self.client.get('/profile/update_profile/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_profile_url(self):
        response = self.client.get('/profile/update_profile')
        self.assertEqual(response.status_code, 301)

    def test_valid_register_user_url(self):
        response = self.client.get('/profile/register_user/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_register_user_url(self):
        response = self.client.get('/profile/register_user')
        self.assertEqual(response.status_code, 301)

    def test_logout(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345678')
        user.save()
        logged_in = self.client.login(username="testuser", password="12345678")
        self.assertEqual(logged_in, True)
        self.client.get('/profile/logout/')


