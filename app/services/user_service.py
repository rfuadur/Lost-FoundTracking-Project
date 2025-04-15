from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)
        
    