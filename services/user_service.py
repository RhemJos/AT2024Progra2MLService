from models.user import User

class UserService:
    def __init__(self):
        self.users = []

    def create_user(self, id, name, email, password):
        new_user = User(id, name, email, password)
        self.users.append(new_user)
        return new_user
    
    def get_all_users(self):
        return [user.to_dict() for user in self.users]
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user.to_dict()
        return None