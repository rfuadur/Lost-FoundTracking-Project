from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String(100))
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    lOrF_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    images = db.Column(db.String(1000))
    status = db.Column(db.Boolean, default=True)
    share_count = db.Column(db.Integer, default=0)
    verification_status = db.Column(db.String(50), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.String(50))
    item_name = db.Column(db.String(100))
    contact_method = db.Column(db.String(50))
    verification_claims = db.relationship("VerificationClaim", backref="post", lazy=True)

    # Relationship with backref and cascade
    chats = db.relationship('Chat', backref=db.backref('chat_post', lazy=True), cascade='all, delete-orphan')
