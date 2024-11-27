from common.exceptions.parameter_exception import ParameterException
from common.validations.validator_strategy import ValidatorStrategy
import json


class JSONFormatValidator(ValidatorStrategy):
    def __init__(self, data):
        self.data = data

    def validate(self):
        try:
            json.loads(self.data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ParameterException(f"Invalid JSON format: {str(e)}")

    def get_status_code(self):
        return 404