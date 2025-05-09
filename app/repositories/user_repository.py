from app.models.user import User
from werkzeug.security import generate_password_hash
from app import db
from sqlalchemy import func

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(name, email, password, contact_info):
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            contact_info=contact_info
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user):
        db.session.commit()
        return user

    def get_top_contributors(self, limit):
        return db.session.query(User)\
        .filter(User.contribution > 0)\
        .order_by(User.contribution.desc())\
        .limit(5).all()

    def count_all(self):
        return User.query.count()

    def count_active(self):
        return User.query.filter_by(is_banned=False).count()

    def count_admins(self):
        return User.query.filter_by(is_admin=True).count()

    def toggle_ban_status(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            user.is_banned = not user.is_banned
            db.session.commit()
            return True
        return False

    def update_ban_status(self, user_id, ban_status):
        user = self.get_by_id(user_id)
        if user:
            user.is_banned = ban_status
            db.session.commit()
            return True
        return False

    def get_recent(self, limit):
        ## user creation logic not set in the model
        pass

    def get_all(self):
        return User.query.all()
