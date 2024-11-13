from flask import jsonify
from abc import ABC, abstractmethod


class ErrorHandlerStrategy(ABC):
    def __init__(self, error_message="An error ocurred", status_code=500):
        self.error_message = error_message
        self.status_code = status_code

    @abstractmethod
    def handle(self):
        pass

    def to_response(self):
        response = {
            "success": False,
            "message": self.error_message
        }
        return jsonify(response), self.status_code
