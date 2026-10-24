from flask import session, current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, name, email, password, contact_info=None):
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered, try different email")

        return self.user_repository.create(name, email, password, contact_info)

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

    def generate_reset_token(self, email):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(email, salt=current_app.config["SECRET_KEY"])

    def verify_reset_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config["SECRET_KEY"],
                max_age=expiration
            )
        except Exception:
            return None
        return email

    def send_reset_email(self, email):
        user = self.user_repository.get_by_email(email)
        if not user:
            return False

        token = self.generate_reset_token(email)
        link = url_for("auth.reset_password", token=token, _external=True)
        
        msg = Message("Password Reset Request",
                      recipients=[user.email])
        msg.body = f"To reset your password, visit the following link: {link}"
        
        # Local import to avoid circular dependency
        from app import mail
        
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            # Fallback for development without email server
            print(f"DEV MODE: Password Reset Link: {link}")
            return True

    def reset_password(self, token, new_password):
        email = self.verify_reset_token(token)
        if not email:
            raise ValueError("Invalid or expired token")
            
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
            
        user.password = generate_password_hash(new_password)
        self.user_repository.update(user)
        return user
