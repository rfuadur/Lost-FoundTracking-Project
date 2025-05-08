from app.models.chat import Chat
from app.models.post import Post
from app.models.verificationClaim import VerificationClaim
from app import db
from sqlalchemy import or_, and_

class ChatRepository:
    @staticmethod
    def get_post_chats(post_id, user_id):
        return Chat.query.filter(
            Chat.post_id == post_id,
            or_(Chat.sender_id == user_id, Chat.receiver_id == user_id)
        ).order_by(Chat.created_at).all()

    @staticmethod
    def get_posts_with_chats(user_id):
        return db.session.query(Post).join(Chat).filter(
            or_(Chat.sender_id == user_id, Chat.receiver_id == user_id)
        ).distinct().all()

    @staticmethod
    def get_verification_claim(post_id, status='approved'):
        return VerificationClaim.query.filter_by(
            post_id=post_id,
            status=status
        ).first()

    @staticmethod
    def get_unread_messages_count(user_id):
        return Chat.query.filter_by(receiver_id=user_id, is_read=False).count()

    @staticmethod
    def mark_messages_read(post_id, user_id):
        messages = Chat.query.filter_by(
            post_id=post_id,
            receiver_id=user_id,
            is_read=False
        ).all()

        if messages:
            for message in messages:
                message.is_read = True
            db.session.commit()

        return len(messages)

    @staticmethod
    def create_message(post_id, sender_id, receiver_id, message_text):
        """Create and save a new chat message"""
        message = Chat(
            post_id=post_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message_text
        )
        db.session.add(message)
        db.session.commit()
        return message
