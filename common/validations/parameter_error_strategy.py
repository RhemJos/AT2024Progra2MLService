from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy


class ParameterErrorStrategy(ValidatorStrategy):
    def __init__(self, error):
        self.error = error

    def validate(self):
        raise ParameterException(str(self.error))

    def get_status_code(self):
        return 400
