from .specific_error_handlers import NotFoundErrorHandler, GenericErrorHandler, InvalidURLErroHandler
from requests.exceptions import HTTPError

class ErrorHandlerFactory:
    @staticmethod
    def get_error_handler(error):
        if isinstance(error, FileNotFoundError):
            return NotFoundErrorHandler(error)
        elif isinstance(error, HTTPError):
            return InvalidURLErroHandler(error)
        return GenericErrorHandler(error)
