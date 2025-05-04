from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.post import Post
from app.models.notification import Notification
from app import db
import logging

class MatchingService:
    def __init__(self):
        try:
            self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            logging.info("Matching service initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing matching service: {e}")
            self.model = None
            
    def compute_text_similarity(self, text1, text2):
        if not text1 or not text2 or not self.model:
            return 0
        
        try:
            # Add more context by combining item properties
            embedding1 = self.model.encode([text1], show_progress_bar=False)[0]
            embedding2 = self.model.encode([text2], show_progress_bar=False)[0]
            similarity = float(cosine_similarity([embedding1], [embedding2])[0][0])
            logging.debug(f"Similarity score: {similarity}")
            return similarity
        except Exception as e:
            logging.error(f"Error computing similarity: {e}")
            return 0
            
    def find_matches(self, post, threshold=0.5):  # Lower threshold for better matches
        try:
            matches = []
            opposite_type = "found" if post.type == "lost" else "lost"
            potential_matches = Post.query.filter_by(type=opposite_type).all()
            
            for candidate in potential_matches:
                if candidate.id == post.id:
                    continue
                    
                post_text = (f"{post.item_name} {post.description} "
                           f"{post.category_name} {post.location}")
                candidate_text = (f"{candidate.item_name} {candidate.description} "
                                f"{candidate.category_name} {candidate.location}")
                
                # Calculate similarity score
                score = self.compute_text_similarity(post_text, candidate_text)
                
                # Add category bonus
                if post.category_name == candidate.category_name:
                    score += 0.2
                
                if score >= threshold:
                    matches.append({'post': candidate, 'score': min(score, 1.0)})
                    logging.info(f"Found match: {candidate.item_name} with score {score}")
            
            return sorted(matches, key=lambda x: x['score'], reverse=True)
        except Exception as e:
            logging.error(f"Error finding matches: {e}")
            return []
        
    def create_match_notification(self, user_id, match_post, original_post, score):
        try:
            # Check if notification already exists
            existing = Notification.query.filter_by(
                user_id=user_id,
                link=f"/posts/post/{match_post.id}"
            ).first()
            
            if not existing:
                notification = Notification(
                    user_id=user_id,
                    title="Potential Match Found!",
                    message=f"We found a {score:.0%} match for your {original_post.type} item '{original_post.item_name}'",
                    link=f"/posts/post/{match_post.id}",
                    is_read=False
                )
                db.session.add(notification)
                db.session.commit()
                logging.info(f"Created notification for user {user_id}")
                
        except Exception as e:
            logging.error(f"Error creating notification: {e}")
            db.session.rollback()
