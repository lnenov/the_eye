import http
import json

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from event_tracker.middleware.shared_secret_authenticator import SharedSecretAuthenticatorMiddleware


class PreSharedSecretAuthenticationTestCase(SimpleTestCase):
    """
    Check that view uses pre shared secret authentication.
    """
    def test_no_header(self):
        response = self.client.post(reverse('event_tracker:event_tracking'))
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    @override_settings(EVENT_TRACKER_SHARED_SECRETS=['AbC'])
    def test_valid_preshared_secret(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbC'
        }
        response = self.client.post(reverse('event_tracker:event_tracking'), **headers)
        self.assertNotEqual(response.status_code, http.HTTPStatus.FORBIDDEN)

    @override_settings(EVENT_TRACKER_SHARED_SECRETS=['AbC'])
    def test_invalid_preshared_secret(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbCc'
        }
        response = self.client.post(reverse('event_tracker:event_tracking'), **headers)
        self.assertEqual(response.status_code, http.HTTPStatus.FORBIDDEN)


class EventHandlingTestCase(SimpleTestCase):
    """
    Check that view uses pre shared secret authentication.
    """
    @override_settings(EVENT_TRACKER_SHARED_SECRETS=['AbC'])
    def test_valid_payload(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbC'
        }
        payload = {
            'session_id': 'Foo-bAr',
            'category': 'page interaction',
            'name': 'pageview',
            'timestamp': '2021-01-01 09:15:27.243860',
            'data': {
                'host': 'main.com',
                'path': '/'
            }
        }
        response = self.client.post(
            reverse('event_tracker:event_tracking'),
            content_type='application/json',
            data=json.dumps(payload),
            **headers
        )
        self.assertEqual(response.status_code, http.HTTPStatus.ACCEPTED)

    @override_settings(EVENT_TRACKER_SHARED_SECRETS=['AbC'])
    def test_invalid_payload(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbC'
        }
        payload = {
            'session_id': 'Foo-bAr',
            'category': 'page interaction',
            'timestamp': '2021-01-01 09:15:27.243860',
            'data': {
                'host': 'main.com',
                'path': '/'
            }
        }
        response = self.client.post(
            reverse('event_tracker:event_tracking'),
            content_type='application/json',
            data=json.dumps(payload),
            **headers
        )
        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)

    @override_settings(EVENT_TRACKER_SHARED_SECRETS=['AbC'])
    def test_invalid_timestamp_payload(self):
        headers = {
            f"HTTP_{SharedSecretAuthenticatorMiddleware.AUTHENTICATION_HEADER}": 'AbC'
        }
        payload = {
            'session_id': 'Foo-bAr',
            'category': 'page interaction',
            'name': 'pageview',
            'timestamp': '2021-01-01X09:15:27.243860',
            'data': {
                'host': 'main.com',
                'path': '/'
            }
        }
        response = self.client.post(
            reverse('event_tracker:event_tracking'),
            content_type='application/json',
            data=json.dumps(payload),
            **headers
        )
        self.assertEqual(response.status_code, http.HTTPStatus.BAD_REQUEST)
