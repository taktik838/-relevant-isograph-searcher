from typing import Dict

# from settings import ENVIRONMENT_VARIABLES


class ServerError(Exception):
    status_code: int = 500
    message: str = 'Что-то пошло не так'
    capture_by_sentry: bool = True

    def __init__(self, debug: str = ''):
        self.debug: str = debug
        super(ServerError, self).__init__(self.message)

    def __str__(self) -> str:
        if self.debug:
            return f'{self.message}. debug: {self.debug}'
        return self.message

    def as_dict(self) -> Dict[str, str]:
        data: Dict[str, str] = {'code': self.__class__.__name__, 'message': self.message}
        # if ENVIRONMENT_VARIABLES.DEBUG:
            # data['debug'] = self.debug
        return data


__all__ = [
    'ServerError',
]
