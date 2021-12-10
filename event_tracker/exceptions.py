import http

from django.http import JsonResponse


class BaseEventTrackerException(Exception):
    def __init__(self, error_message, *args, **kwargs):
        self.error_message = error_message
        super().__init__(*args, **kwargs)

    def as_response(self, status=http.HTTPStatus.BAD_REQUEST):
        response_data = {
            'error': self.error_message
        }
        return JsonResponse(response_data, status=status)


class EventValidationError(BaseEventTrackerException):
    pass
