import abc
import inspect

import dateutil.parser

from event_tracker.exceptions import EventValidationError


class _BaseEventValidator:
    __metaclass__ = abc.ABCMeta
    _REQUIRED_FIELDS = [
        'category',
        'name',
        'session_id',
        'timestamp',
        'data',
    ]

    @property
    @abc.abstractmethod
    def NAME(self):
        pass

    @classmethod
    def _validate_common(cls, payload):
        for required_field in cls._REQUIRED_FIELDS:
            if required_field not in payload:
                raise EventValidationError(f'{required_field} missing')

        try:
            dateutil.parser.parse(payload['timestamp'])
        except dateutil.parser._parser.ParserError:
            raise EventValidationError('Timestamp format is not readable')

    @abc.abstractclassmethod
    def _validate_data(cls, payload):
        pass

    @classmethod
    def validate(cls, payload):
        cls._validate_common(payload)
        cls._validate_data(payload)


class _PageInteractionEventValidator(_BaseEventValidator):
    NAME = 'page interaction'
    _DATA_FIELDS = [
        'host',
        'path',
        'element'
    ]

    @classmethod
    def _validate_data(cls, payload):
        for required_field in cls._DATA_FIELDS:
            if required_field not in payload['data']:
                raise EventValidationError(f'{required_field} missing')


class _PageViewEventValidator(_BaseEventValidator):
    NAME = 'pageview'
    _DATA_FIELDS = [
        'host',
        'path'
    ]

    @classmethod
    def _validate_data(cls, payload):
        for required_field in cls._DATA_FIELDS:
            if required_field not in payload['data']:
                raise EventValidationError(f'{required_field} missing')


class _EventValidator:
    def __init__(self):
        self.event_validators_per_name = {}
        for name, var in globals().items():
            if inspect.isclass(var) and var is not _BaseEventValidator and issubclass(var, _BaseEventValidator):
                self.event_validators_per_name[var.NAME] = var

    def __call__(self, payload):
        try:
            event_validator = self.event_validators_per_name[payload['name']]
        except KeyError:
            raise EventValidationError('Event name not recognized')
        else:
            event_validator.validate(payload)


event_validator = _EventValidator()
