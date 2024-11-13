from flask import jsonify
from requests import HTTPError
from .error_handler_strategy import ErrorHandlerStrategy


class NotFoundErrorHandler(ErrorHandlerStrategy):
    def __init__(self, error):
        super().__init__(str(error), status_code=404)

    def handle(self):
        return self.to_response()


class GenericErrorHandler(ErrorHandlerStrategy):
    def __init__(self, error):
        status_code = 404 if isinstance(error, HTTPError) else 500
        super().__init__(str(error), status_code=status_code)

    def handle(self):
        return self.to_response()


class InvalidURLErroHandler(ErrorHandlerStrategy):
    def __init__(self, error):
        super().__init__(str(error), status_code=404)

    def handle(self):
        return self.to_response()
