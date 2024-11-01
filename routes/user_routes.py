from flask import Blueprint, request
from controllers.user_controller import UserController

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users', methods=['POST'])
def create_user():
    return UserController.create_user()


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    return UserController.get_users()


@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)
