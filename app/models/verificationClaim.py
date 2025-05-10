from app import db
from datetime import datetime
from sqlalchemy import event

class VerificationClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String(50), default="pending")
    proof_details = db.Column(db.String(1000))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    verification_score = db.Column(db.Float, default=0.0)
    user = db.relationship("User", backref="verification_claims", foreign_keys=[user_id])

@event.listens_for(VerificationClaim.status, 'set')
def increment_contribution_on_approve(target, value, oldvalue, initiator):
    if value == "approved" and oldvalue != "approved":
        user = target.user  # Get the user who created the post
        if user:
            user.contribution += 1
