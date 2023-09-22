from fastapi import status

from app.api.exceptions import utils


class AppException(Exception):
    STATUS: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    CODE: str = 'UNKNOWN'
    DEFAULT_MESSAGE: str = 'Oops, something went wrong!'

    def __init__(self, message: str | None = None):
        message = utils.add_missing_punctuation(message or self.DEFAULT_MESSAGE)
        super().__init__(message)


class NotFoundException(AppException):
    STATUS: int = status.HTTP_404_NOT_FOUND
    CODE: str = 'NOT_FOUND'
    DEFAULT_MESSAGE: str = 'Resource not found'


class BadRequestException(AppException):
    STATUS: int = status.HTTP_400_BAD_REQUEST


class BadRequestFieldException(BadRequestException):
    def __init__(self, field: str, message: str | None = None):
        self.field = field
        super().__init__(message)


class AggregateException(BadRequestException):
    def __init__(self, exceptions: list[AppException]):
        self.exceptions = exceptions


class InvalidResponseHandlerException(AppException):
    CODE: str = 'INVALID_RESPONSE_HANDLER'
    DEFAULT_MESSAGE: str = 'Invalid response handler'
