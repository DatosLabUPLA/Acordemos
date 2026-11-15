from django.urls import reverse
from social_core.backends.google import GoogleOAuth2


class GoogleOAuth2Callback(GoogleOAuth2):
    def __init__(self, strategy=None, redirect_uri=None):
        if redirect_uri is not None:
            redirect_uri = reverse('google-oauth-callback')
        super().__init__(strategy, redirect_uri)
