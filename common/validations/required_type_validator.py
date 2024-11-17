from common.validations.validator_strategy import ValidatorStrategy
from common.exceptions.parameter_exception import ParameterException


class RequiredTypeValidator(ValidatorStrategy):
    def __init__(self, field, data, expected_types):
        self.field = field
        self.data = data
        # Asegúrate de que 'expected_types' es un tuple
        self.expected_types = expected_types if isinstance(expected_types, tuple) else (expected_types,)

    def validate(self):
        if self.data is None:
            message = f"The parameter '{self.field}' is required."
            raise ParameterException(message)
        
        # Validar si el tipo de dato es uno de los tipos esperados
        if not isinstance(self.data, self.expected_types):
            message = f"The parameter '{self.field}' is expected to be of type {self._type_name()}"
            raise ParameterException(message)
        
    def get_status_code(self):
        return 400
    
    def _type_name(self):
        # Usar 'self.expected_types' para el caso con múltiples tipos
        if isinstance(self.expected_types, tuple):
            return " or ".join(t.__name__ for t in self.expected_types)
        return self.expected_types.__name__
