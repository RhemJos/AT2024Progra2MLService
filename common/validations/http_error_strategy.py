from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy


class HTTPErrorStrategy(ValidatorStrategy):
    def __init__(self, error):
        self.error = error

    def validate(self):
        status_code = self.error.response.status_code
        message = f"{status_code} Client Error: {self.error.response.reason} for url: {self.error.response.url}"
        raise ParameterException(message)

    def get_status_code(self):
        return self.error.response.status_code
