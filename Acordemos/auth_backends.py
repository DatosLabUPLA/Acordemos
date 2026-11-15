from django.urls import reverse
from social_core.backends.google import GoogleOAuth2


class GoogleOAuth2Callback(GoogleOAuth2):
    ACCESS_TOKEN_URL = 'https://oauth2.googleapis.com/token'

    def __init__(self, strategy=None, redirect_uri=None):
        if redirect_uri is not None:
            redirect_uri = reverse('google-oauth-callback')
        super().__init__(strategy, redirect_uri)

    def user_data(self, access_token, *args, **kwargs):
        profile = self.get_json(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': 'Bearer ' + access_token},
        )
        profile['id'] = profile['sub']
        return profile
