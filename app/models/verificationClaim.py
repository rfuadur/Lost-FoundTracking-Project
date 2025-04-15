from app import db
from datetime import datetime

class VerificationClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String(50), default="pending")
    proof_details = db.Column(db.String(1000))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    verification_score = db.Column(db.Float, default=0.0)
    user = db.relationship("User", backref="verification_claims", foreign_keys=[user_id])