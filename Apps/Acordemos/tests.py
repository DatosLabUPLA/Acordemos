from urllib.parse import parse_qs, urlsplit

from django.test import SimpleTestCase, override_settings


@override_settings(
    ALLOWED_HOSTS=['acordemos.datoslab.cl'],
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='test-client',
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='test-secret',
)
class AuthenticationTests(SimpleTestCase):
    def test_admin_login_loads(self):
        response = self.client.get(
            '/admin/login/', {'next': '/admin/'},
            HTTP_HOST='acordemos.datoslab.cl', secure=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_google_login_uses_custom_callback(self):
        response = self.client.get(
            '/auth/login/google-oauth2/',
            HTTP_HOST='acordemos.datoslab.cl', secure=True,
        )
        self.assertEqual(response.status_code, 302)
        params = parse_qs(urlsplit(response['Location']).query)
        self.assertEqual(
            params['redirect_uri'],
            ['https://acordemos.datoslab.cl/auth/google/callback'],
        )
