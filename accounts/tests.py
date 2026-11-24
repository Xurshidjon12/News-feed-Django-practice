from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginRoutingTests(TestCase):
    def test_password_change_redirects_to_login(self):
        response = self.client.get(reverse('password_change'))

        self.assertRedirects(
            response,
            '/account/login/?next=/account/password-change/',
        )

    def test_default_login_path_preserves_next(self):
        response = self.client.get(
            '/accounts/login/', {'next': reverse('password_change')}
        )

        self.assertRedirects(
            response,
            '/account/login/?next=%2Faccount%2Fpassword-change%2F',
        )

    def test_login_returns_to_requested_page(self):
        get_user_model().objects.create_user(username='reader', password='password123')

        response = self.client.post(
            '/account/login/?next=/account/password-change/',
            {'username': 'reader', 'password': 'password123'},
        )

        self.assertRedirects(response, reverse('password_change'), fetch_redirect_response=False)
