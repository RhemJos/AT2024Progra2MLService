from flask import jsonify
from requests.exceptions import HTTPError
from common.exceptions.parameter_exception import ParameterException
from common.validations.context import Context
from common.validations.file_not_found_strategy import FileNotFoundStrategy
from common.validations.generic_exception_strategy import GenericExceptionStrategy
from common.validations.http_error_strategy import HTTPErrorStrategy


class ErrorHandlerFacade:
    def __init__(self):
        self.strategies = {
            FileNotFoundError: FileNotFoundStrategy,
            HTTPError: HTTPErrorStrategy,
            Exception: GenericExceptionStrategy
        }

    def handle_error(self, error):
        error_type = type(error)
        if error_type in self.strategies:
            strategy_class = self.strategies[error_type]
            strategy = strategy_class(error)
            context = Context([strategy])
            try:
                context.validate()
            except ParameterException as e:
                return jsonify({"success": False, "message": str(e)}), strategy.get_status_code()
        else:
            return jsonify({"success": False, "message": f"Unhandled error: {str(error)}"}), 500
