from datetime import datetime
import os
from app.repositories.post_repository import PostRepository
from app.utils.image_utils import save_image, save_images
from app.models.post import Post

class PostService:
    def __init__(self):
        self.post_repository = PostRepository()

<<<<<<< Updated upstream
   
    def get_user_stats(self, user_id):
        user_posts = self.post_repository.get_by_user_id(user_id)
        lost_items = [p for p in user_posts if p.type == "lost"]
        found_items = [p for p in user_posts if p.type == "found"]
        
        return {
            'total_posts': len(user_posts),
            'lost_items': len(lost_items),
            'found_items': len(found_items)
        }
    
    def get_recent_activities(self, limit=5):
        return self.post_repository.get_recent(limit)

    def get_by_type_and_user(self, type_name, user_id):
        return Post.query.filter_by(
            type=type_name,
            user_id=user_id
        ).order_by(Post.post_date.desc()).all()

    def get_by_id(self, post_id):
        return self.post_repository.get_by_id(post_id)

    def get_by_user_id(self, user_id):
        return self.post_repository.get_by_user_id(user_id)
=======
    
    def create_lost_item(self, form_data, files, user_id):
        data = {
            'category_name': form_data.get('category'),
            'item_name': form_data.get('item_name'),
            'description': form_data.get('description'),
            'lOrF_date': datetime.strptime(form_data.get('lost_date'), '%Y-%m-%d'),
            'post_date': datetime.utcnow,
            'location': form_data.get('place_lost'),
            'contact_method': form_data.get('contact_method'),
            'type': 'lost',
            'user_id': user_id
        }
        
        if 'image' in files:
            data['images'] = save_image(files['image'])
            
        return self.post_repository.create(data)

    def create_found_item(self, form_data, files, user_id):
        data = {
            'category_name': form_data.get('category'),
            'item_name': form_data.get('item_name'),
            'description': form_data.get('description'),
            'lOrF_date': datetime.strptime(form_data.get('found_date'), '%Y-%m-%d'),
            'post_date': datetime.utcnow,
            'location': form_data.get('place_found'),
            'contact_method': form_data.get('contact_method'),
            'type': 'found',
            'user_id': user_id
        }
        
        if 'image' in files:
            data['images'] = save_image(files['image'])
            
        return self.post_repository.create(data)
>>>>>>> Stashed changes
