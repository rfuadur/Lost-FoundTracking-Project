from app.models.post import Post
from app.models.verificationClaim import VerificationClaim
from sqlalchemy import desc
from app import db

class VerificationRepository:
    def get_claims_by_post_owner(self, user_id):
        """Get claims for posts owned by user"""
        return (VerificationClaim.query
                .join(Post, VerificationClaim.post_id == Post.id)
                .filter(Post.user_id == user_id)
                .order_by(desc(VerificationClaim.submission_date))
                .all())

    def get_by_post_and_user(self, post_id, user_id):
        """Get claim by post and user IDs"""
        return VerificationClaim.query.filter_by(
            post_id=post_id,
            user_id=user_id
        ).first()

    def create_claim(self, data):
        """Create new verification claim"""
        claim = VerificationClaim(**data)
        db.session.add(claim)
        db.session.commit()
        return claim

    def get_pending_claims_count(self, user_id):
        """Get count of pending claims for user's posts"""
        return (VerificationClaim.query.join(Post)
                .filter(Post.user_id == user_id,
                       VerificationClaim.status == 'pending')
                .count())

    def update_claim_status(self, claim_id, new_status):
        """Update claim status"""
        claim = self.get_by_id(claim_id)
        if claim:
            claim.status = new_status
            db.session.commit()
        return claim

    def get_claims_by_post(self, post_id):
        """Get all claims for a specific post"""
        return VerificationClaim.query.filter_by(post_id=post_id).all()

    def get_by_id(self, claim_id):
        """Get claim by ID"""
        return VerificationClaim.query.get(claim_id)

    def get_claim_by_status(self, post_id, status, user_id=None):
        """Get claim by post ID and status, optionally filtered by user ID"""
        query = VerificationClaim.query.filter_by(
            post_id=post_id,
            status=status
        )

        if user_id is not None:
            query = query.filter_by(user_id=user_id)

        return query.first()

    @staticmethod
    def get_claim_by_post_and_user(post_id, user_id):
        """Get a verification claim for a specific post and user"""
        return VerificationClaim.query.filter_by(
            post_id=post_id,
            user_id=user_id
        ).first()
