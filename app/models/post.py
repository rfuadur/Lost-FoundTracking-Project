from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
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
