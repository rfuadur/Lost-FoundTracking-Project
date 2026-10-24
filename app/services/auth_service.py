import logging
import requests
from flask import session, current_app, url_for
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories.user_repository import UserRepository

# Mailjet's HTTPS Send API (Render's free tier blocks outbound SMTP ports)
MAILJET_SEND_URL = "https://api.mailjet.com/v3.1/send"

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

        api_key = current_app.config.get("MAILJET_API_KEY")
        secret_key = current_app.config.get("MAILJET_SECRET_KEY")
        sender = current_app.config.get("MAIL_SENDER")
        if not (api_key and secret_key and sender):
            logging.warning("Mailjet is not configured; password reset email not sent.")
            # Fallback for local development without Mailjet credentials
            if current_app.debug:
                logging.warning(f"DEV MODE: Password Reset Link: {link}")
            return False

        payload = {
            "Messages": [{
                "From": {"Email": sender, "Name": current_app.config["MAIL_SENDER_NAME"]},
                "To": [{"Email": user.email, "Name": user.name}],
                "Subject": "Password Reset Request",
                "TextPart": (
                    f"To reset your password, visit the following link: {link}\n\n"
                    "This link expires in 1 hour. If you didn't request a reset, you can ignore this email."
                ),
            }]
        }

        try:
            response = requests.post(MAILJET_SEND_URL, auth=(api_key, secret_key), json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            detail = e.response.text if e.response is not None else e
            logging.error(f"Error sending password reset email via Mailjet: {detail}")
            return False

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
