from django.test import TestCase, client


class AppNavigationTest(TestCase):
    def setUp(self):
        self.client = client.Client()

    def test_valid_login_url(self):
        response = self.client.get('/profile/login/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_url(self):
        response = self.client.get('/profile/login')
        self.assertEqual(response.status_code, 301)

    def test_valid_change_password_url(self):
        response = self.client.get('/profile/change_password/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_change_password_url(self):
        response = self.client.get('/profile/change_password')
        self.assertEqual(response.status_code, 301)

    def test_valid_update_profile_url(self):
        response = self.client.get('/profile/update_profile/')
        self.assertEqual(response.status_code, 302)

    def test_invalid_update_profile_url(self):
        response = self.client.get('/profile/update_profile')
        self.assertEqual(response.status_code, 301)

    def test_valid_register_user_url(self):
        response = self.client.get('/profile/register_user/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_register_user_url(self):
        response = self.client.get('/profile/register_user')
        self.assertEqual(response.status_code, 301)

    def test_logout_url(self):
        response = self.client.get('/profile/logout/')
        self.assertEqual(response.status_code, 302)


