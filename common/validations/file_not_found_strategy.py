from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy


class FileNotFoundStrategy(ValidatorStrategy):
    def __init__(self, error):
        self.error = error

    def validate(self):
        raise ParameterException(f"File not found: {str(self.error)}")

    def get_status_code(self):
        return 404