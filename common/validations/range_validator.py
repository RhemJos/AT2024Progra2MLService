from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy


class RangeValidator(ValidatorStrategy):
    def __init__(self, field, value, min_value, max_value):
        self.field = field
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def validate(self):
        if not (self.min_value <= self.value <= self.max_value):
            message = f"The parameter {self.field} must be between {self.min_value} and {self.max_value}."
            raise ParameterException(message)
        
    def get_status_code(self):
        return 400