from app import db
from datetime import datetime

class UserReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    claim_id = db.Column(db.Integer, db.ForeignKey("verification_claim.id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    type = db.Column(db.String(50), nullable=False)  # verification, chat, post
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    admin_notes = db.Column(db.String(500))
