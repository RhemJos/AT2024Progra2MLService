from common.validations.validator_strategy import ValidatorStrategy
from common.exceptions.parameter_exception import ParameterException


class TypeValidator(ValidatorStrategy):
    def __init__(self, field, data, expected_type):
        self.field = field
        self.data = data
        self.expected_type = expected_type

    def validate(self):
        if not isinstance(self.data, self.expected_type):
            message = f"The parameter {self.field} is expected to be of type {self.expected_type.__name__}"
            raise ParameterException(message)
        
    def get_status_code(self):
        return 400