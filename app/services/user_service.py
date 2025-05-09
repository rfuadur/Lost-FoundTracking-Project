from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def get_by_email(self, email):
        return self.user_repository.get_by_email(email)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_user(self, user_id, data):
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in data.items():
            setattr(user, key, value)

        return self.user_repository.update(user)

    def get_notifications(self, user_id):
        # TODO: Implement notifications system
        return []
