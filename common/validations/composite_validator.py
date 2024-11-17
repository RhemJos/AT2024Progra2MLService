from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy


class CompositeValidator(ValidatorStrategy):
    def __init__(self, validations):
        self.validations = validations
        self.errors = []

    def validate(self):
        for validator in self.validations:
            try:
                validator.validate()
            except ParameterException as e:
                self.errors.append(str(e))

        if self.errors:
            error_message = "Validation failed for the following parameters: " + "; ".join(self.errors)
            raise ParameterException(error_message)

    def get_status_code(self):
        return 400