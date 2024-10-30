from services.user_service import UserService
from flask import request

user_service = UserService()


class UserController:
    @staticmethod
    def create_user():
        data = request.get_json()
        id = data.get("id")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        return user_service.create_user(id, name, email, password)

    @staticmethod
    def get_users():
        return user_service.get_all_users()

    @staticmethod
    def get_user(user_id):
        return user_service.get_user_by_id(user_id)
