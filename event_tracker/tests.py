import http

from django.test import SimpleTestCase
from django.urls import reverse

from event_tracker.middleware.shared_secret_authenticator import SharedSecretAuthenticatorMiddleware


class PreSharedSecretAuthenticationMiddlewareTests(SimpleTestCase):
    """
    Uses the plaleholder view to test the middleware.
    """
    def test_no_header(self):
        response = self.client.get(reverse('event_tracker:index'))
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

        response = self.client.post(reverse('event_tracker:index'))
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    def test_valid_preshared_secret(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbC'
        }
        response = self.client.get(reverse('event_tracker:index'), **headers)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        response = self.client.post(reverse('event_tracker:index'), **headers)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_invalid_preshared_secret(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbCc'
        }
        response = self.client.get(reverse('event_tracker:index'), **headers)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

        response = self.client.post(reverse('event_tracker:index'), **headers)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)
