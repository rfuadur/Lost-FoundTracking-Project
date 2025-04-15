from app import db
from datetime import datetime

class UserReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
