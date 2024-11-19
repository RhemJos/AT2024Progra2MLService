from common.validations.validator_strategy import ValidatorStrategy
from common.exceptions.parameter_exception import ParameterException


class EmptyOrNoneValidator(ValidatorStrategy):
    def __init__(self, field, data):
        self.field = field
        self.data = data

    def validate(self):
        if self.data is None:
            message = f"The parameter {self.field} doesn't exist"
            raise ParameterException(message)
        elif str(self.data).strip() == '':
            message = f"The parameter {self.field} is invalid"
            raise ParameterException(message)

    def get_status_code(self):
        return 400