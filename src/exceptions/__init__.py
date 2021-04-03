from .base import ServerError


class MethodNotImplemented(ServerError):
    status_code = 400
    message = 'Метод еще не реализован'
    capture_by_sentry = False


class ValidationError(ServerError):
    status_code = 400
    message = 'Ошибка проверки данных'
    capture_by_sentry = False


class NotFound(ServerError):
    status_code = 404
    message = 'Ресурс не найден'
    capture_by_sentry = False


class Forbidden(ServerError):
    status_code = 403
    message = 'Доступ запрещён'
    capture_by_sentry = False


class InputValidationError(ServerError):
    status_code = 400
    message = 'Некорректный запрос'
    capture_by_sentry = False


class AddEntityToBDError(ServerError):
    status_code = 409
    message = 'Ошибка добавления записи в бд'
    capture_by_sentry = False
