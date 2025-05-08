import json
from app.repositories.verification_repository import VerificationRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService
from app.utils.image_utils import save_image


class VerificationService:
    def __init__(self):
        self.verification_repository = VerificationRepository()
        self.post_repository = PostRepository()
        self.user_repository = UserRepository()
        self.notification_service = NotificationService()

    def get_post(self, post_id):
        return self.post_repository.get_by_id(post_id)

    def create_verification_claim(self, post_id, user_id, form_data, files):
        # Check for existing claim
        existing_claim = self.verification_repository.get_by_post_and_user(post_id, user_id)
        if existing_claim:
            raise ValueError("You have already submitted a claim for this item")

        proof_files = []
        if files:
            for file in files.getlist('proof_files'):
                if file.filename:
                    filename = save_image(file)
                    if filename:
                        proof_files.append(filename)

        claim_data = {
            'post_id': post_id,
            'user_id': user_id,
            'proof_details': json.dumps({
                'lost_location': form_data.get('lost_location'),
                'lost_date': form_data.get('lost_date'),
                'unique_identifier': form_data.get('unique_identifier'),
                'additional_proof': form_data.get('additional_proof'),
                'proof_files': proof_files
            })
        }

        return self.verification_repository.create_claim(claim_data)


    def get_user_claims(self, user_id):
        """Get all verification claims for user's posts with associated data"""
        claims = self.verification_repository.get_claims_by_post_owner(user_id)
        claims_data = []

        for claim in claims:
            post = self.post_repository.get_by_id(claim.post_id)
            user = self.user_repository.get_by_id(claim.user_id)

            claims_data.append({
                'claim': claim,
                'post': post,
                'user': user
            })

        return claims_data


    def update_claim_status(self, claim_id, post_id, new_status):
        """Update claim status and handle notifications"""
        claim = self.verification_repository.update_claim_status(claim_id, new_status)
        if claim:
            post = self.post_repository.get_by_id(post_id)
            if new_status == 'approved':
                post.verification_status = 'verified'
                self.post_repository.update(post)
                # Return data needed for chat notifications
                return {
                    'claim_user_id': claim.user_id,
                    'post_user_id': post.user_id,
                    'post_id': post.id,
                    'post_name': post.item_name
                }

            message = f"Your verification claim for '{post.item_name}' has been {new_status}"
            self.notification_service.create_verification_notification(
                claim.user_id,
                message,
                f'/posts/post/{post_id}'
            )
            return True
        return False


    def get_post_claims(self, post_id):
        """Get all claims for a specific post with user data"""
        claims = self.verification_repository.get_claims_by_post(post_id)
        claims_data = []

        for claim in claims:
            user = self.user_repository.get_by_id(claim.user_id)
            proof_data = json.loads(claim.proof_details)
            claims_data.append({
                'claim': claim,
                'user': user,
                'proof_data': proof_data
            })

        return claims_data


    def get_approved_claim(self, post_id):
        """Get the approved claim for a post with user data"""
        claim = self.verification_repository.get_claim_by_status(post_id=post_id, status='approved')
        if claim:
            user = self.user_repository.get_by_id(claim.user_id)
            return {'claim': claim, 'user': user}
        return None


    def get_user_post_claim(self, post_id, user_id):
        """Get a user's claim for a specific post"""
        return self.verification_repository.get_claim_by_post_and_user(post_id, user_id)
