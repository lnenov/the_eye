import collections
import http
import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views import View

from event_tracker.validators import event_validator
from event_tracker.exceptions import BaseEventTrackerException

logger = logging.getLogger(__name__)


def _flatten(dictionary, parent_key='', sep='_'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(_flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))

    return dict(items)


class EventTrackingView(View):
    def post(self, request):
        if request.content_type.lower() != 'application/json':
            return HttpResponse(status=http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        try:
            payload = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse(status=http.HttpStatus.BAD_REQUEST)

        try:
            event_validator(payload)
        except BaseEventTrackerException as event_tracker_exception:
            response = event_tracker_exception.as_response()
        else:
            self.log_event(payload)
            response = JsonResponse(data={}, status=http.HTTPStatus.ACCEPTED)

        return response

    def log_event(self, event):
        log_message = ' '.join([f'{key}={value}' for key, value in _flatten(event).items()])
        logger.info(log_message)
