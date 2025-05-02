from app.models.verificationClaim import VerificationClaim
from app.models.post import Post
from app import db

class VerificationRepository:
    def get_claim(self, claim_id):
        return VerificationClaim.query.get_or_404(claim_id)

    def get_claims_for_post(self, post_id):
        return VerificationClaim.query.filter_by(post_id=post_id).all()

    def has_approved_claim(self, post_id, user_id):
        return VerificationClaim.query.filter_by(
            post_id=post_id,
            user_id=user_id,
            status='approved'
        ).first() is not None

    def get_approved_claim(self, post_id):
        """Get the first approved claim for a post"""
        return VerificationClaim.query.filter_by(
            post_id=post_id,
            status='approved'
        ).first()

    def create_claim(self, claim_data):
        claim = VerificationClaim(**claim_data)
        db.session.add(claim)
        db.session.commit()
        return claim

    def update_claim_status(self, claim_id, status):
        claim = self.get_claim(claim_id)
        claim.status = status
        db.session.commit()
        return claim

    #need to add notification system
