from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from django.test import TestCase, override_settings
from social_django.models import UserSocialAuth

from Acordemos.auth_backends import GoogleOAuth2Callback


@override_settings(
    ALLOWED_HOSTS=['acordemos.datoslab.cl'],
    SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies',
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='test-client',
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='test-secret',
)
class AuthenticationTests(TestCase):
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

    def test_google_callback_exchanges_code_and_starts_session(self):
        host = 'acordemos.datoslab.cl'
        start = self.client.get('/auth/login/google-oauth2/', HTTP_HOST=host, secure=True)
        state = parse_qs(urlsplit(start['Location']).query)['state'][0]
        profile = {'sub': 'test-subject', 'email': 'test@example.org'}

        with patch.object(GoogleOAuth2Callback, 'request_access_token',
                          return_value={'access_token': 'test-token'}) as exchange:
            with patch.object(GoogleOAuth2Callback, 'get_json',
                              return_value=profile) as userinfo:
                response = self.client.get(
                    '/auth/google/callback', {'code': 'test-code', 'state': state},
                    HTTP_HOST=host, secure=True,
                )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(exchange.call_args[0][0], 'https://oauth2.googleapis.com/token')
        self.assertEqual(
            exchange.call_args[1]['data']['redirect_uri'],
            'https://acordemos.datoslab.cl/auth/google/callback',
        )
        userinfo.assert_called_once_with(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': 'Bearer test-token'},
        )
        association = UserSocialAuth.objects.get(provider='google-oauth2', uid=profile['email'])
        self.assertEqual(self.client.session['_auth_user_id'], str(association.user_id))
