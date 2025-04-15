from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
from app.models.user import User

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, name, email, password, contact_info=None):
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered")
            
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            contact_info=contact_info
        )
        return self.user_repository.create(user)

    def authenticate(self, email, password):
        user = self.user_repository.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None
        if user.is_banned:
            raise ValueError("Account is suspended")
        return user
        
    def login_user(self, user):
        session["user_id"] = user.id
        session["user_name"] = user.name
        session["is_admin"] = user.is_admin
        session.permanent = True
        
    def logout_user(self):
        session.clear()
