import json
from flask import url_for
from app.models.verificationClaim import VerificationClaim
from app.repositories.verification_repository import VerificationRepository
from app.repositories.post_repository import PostRepository
from app.utils.image_utils import save_image
from app import db

class VerificationService:
    def __init__(self):
        self.verification_repository = VerificationRepository()
        self.post_repository = PostRepository()

    def get_post(self, post_id):
        return self.post_repository.get_by_id(post_id)

    def get_claims_for_post(self, post_id):
        claims = self.verification_repository.get_claims_for_post(post_id)
        return [{
            'claim': claim,
            'user': claim.user,
            'proof_data': json.loads(claim.proof_details)
        } for claim in claims]

    def create_verification_claim(self, post_id, user_id, form_data, files):
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

    def update_claim_status(self, post_id, claim_id, new_status):
        claim = self.verification_repository.get_claim(claim_id)
        post = self.post_repository.get_by_id(post_id)

        if new_status == 'approved':
            post.verification_status = 'verified'
            self.post_repository.update(post)

            # Create notifications
            

        return self.verification_repository.update_claim_status(claim_id, new_status)

    #need to add notification system
        
