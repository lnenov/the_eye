from django.conf import settings
from django.core.exceptions import PermissionDenied


class SharedSecretAuthenticatorMiddleware(object):
    """
    Basic authentication based on pre shared secrets
    """
    AUTHENTICATION_HEADER = 'X-AUTH'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        received_preshared_secret = request.headers.get(self.AUTHENTICATION_HEADER)

        if received_preshared_secret not in settings.EVENT_TRACKER_SHARED_SECRETS:
            raise PermissionDenied()

        response = self.get_response(request)

        return response
