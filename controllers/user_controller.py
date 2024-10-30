from services.user_service import UserService
from flask import request

user_service = UserService()


class UserController:
    @staticmethod
    def create_user():
        id = request.get_json("id")
        name = request.get_json("name")
        email = request.get_json("email")
        password = request.get_json("password")
        new_user = user_service.create_user(id, name, email, password)
        return new_user.to_dictionary()

    @staticmethod
    def get_users():
        return user_service.get_all_users()

    @staticmethod
    def get_user(user_id):
        return user_service.get_user_by_id(user_id)
