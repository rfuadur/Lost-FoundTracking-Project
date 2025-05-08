from app import db, socketio
from datetime import datetime

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    # Relationships
    post = db.relationship('Post')
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_chats')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_chats')

    @classmethod
    def mark_messages_read(cls, post_id, user_id):
        """Class method to mark messages as read and emit the update"""
        messages = cls.query.filter_by(
            post_id=post_id,
            receiver_id=user_id,
            is_read=False
        ).all()

        if messages:
            for message in messages:
                message.is_read = True
            db.session.commit()

            # Emit to all clients in the room
            socketio.emit('messages_read', {
                'post_id': post_id,
                'reader_id': user_id,
                'room': f'post_{post_id}'
            })

        return len(messages)
