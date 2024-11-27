from abc import ABC, abstractmethod


class ValidatorStrategy(ABC):
    @abstractmethod
    def validate(self):
        """Validate method should be implemented"""

    @abstractmethod
    def get_status_code(self):
        """Return the appropriate HTTP status code"""