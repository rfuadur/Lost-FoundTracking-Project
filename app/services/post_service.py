from datetime import datetime
import os
import pytz
import logging
from app.repositories.post_repository import PostRepository
from app.utils.image_utils import save_image, save_images
from app.services.matching_service import MatchingService

class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
        self.matching_service = MatchingService()
        self.local_tz = pytz.timezone('Asia/Dhaka') # Set Asia/Dhaka timezone

    def get_all_lost_items(self):
        return self.post_repository.get_by_type("lost")

    def get_all_found_items(self):
        return self.post_repository.get_by_type("found")

    def get_user_stats(self, user_id):
        user_posts = self.post_repository.get_by_user_id(user_id)
        lost_items = [p for p in user_posts if p.type == "lost"]
        found_items = [p for p in user_posts if p.type == "found"]

        return {
            'total_posts': len(user_posts),
            'lost_items': len(lost_items),
            'found_items': len(found_items)
        }

    def get_by_type_and_user(self, type_name, user_id):
        return self.post_repository.get_by_type_and_user(type_name, user_id)

    def get_by_id(self, post_id):
        return self.post_repository.get_by_id(post_id)

    def get_by_user_id(self, user_id):
        return self.post_repository.get_by_user_id(user_id)

    def create_lost_item(self, form_data, files, user_id):
        lost_date = datetime.strptime(form_data.get('lost_date'), '%Y-%m-%d')
        lost_date = self.local_tz.localize(lost_date)
        post_date = datetime.now(self.local_tz)

        data = {
            'category_name': form_data.get('category'),
            'item_name': form_data.get('item_name'),
            'description': form_data.get('description'),
            'lOrF_date': lost_date,
            'post_date': post_date,
            'location': form_data.get('place_lost'),
            'contact_method': form_data.get('contact_method'),
            'type': 'lost',
            'user_id': user_id
        }

        if 'image' in files:
            data['images'] = save_image(files['image'])

        post = self.post_repository.create(data)
        self.process_matches(post)
        return post

    def create_found_item(self, form_data, files, user_id):
        found_date = datetime.strptime(form_data.get('found_date'), '%Y-%m-%d')
        found_date = self.local_tz.localize(found_date)
        post_date = datetime.now(self.local_tz)

        data = {
            'category_name': form_data.get('category'),
            'item_name': form_data.get('item_name'),
            'description': form_data.get('description'),
            'lOrF_date': found_date,
            'post_date': post_date,
            'location': form_data.get('place_found'),
            'contact_method': form_data.get('contact_method'),
            'type': 'found',
            'user_id': user_id
        }

        if 'image' in files:
            data['images'] = save_image(files['image'])

        post = self.post_repository.create(data)
        self.process_matches(post)
        return post

    def update(self, post, form_data=None, files=None):
        try:
            if form_data:
                post.description = form_data.get('description', post.description)
                post.category_name = form_data.get('category', post.category_name)
                post.location = form_data.get('location', post.location)

            if files and 'images' in files:
                new_images = save_images(files)
                if new_images:
                    post.images = new_images

            return self.post_repository.update(post)
        except Exception as e:
            print(f"Error updating post: {str(e)}")
            raise

    def delete(self, post):
        try:
            # Delete the post's images from storage if they exist
            if post.images:
                for image_name in post.images.split(','):
                    try:
                        image_path = os.path.join('static', 'uploads', image_name)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    except Exception as e:
                        print(f"Error deleting image {image_name}: {str(e)}")

            # Delete the post from database
            return self.post_repository.delete(post)
        except Exception as e:
            print(f"Error deleting post: {str(e)}")
            raise

    def process_matches(self, post):
        """Find and notify users about potential matches"""
        try:
            print(f"Processing matches for post {post.id}")  # Debug log
            matches = self.matching_service.find_matches(post)
            print(f"Matches found: {matches}")  # Debug log

            if matches:
                print(f"Found {len(matches)} potential matches")  # Debug log

                # Get top 3 matches and notify users
                for match in matches[:3]:
                    print(f"Creating notifications for match with score {match['score']}")  # Debug log

                    # Notify the original post owner
                    self.matching_service.create_match_notification(
                        post.user_id,
                        match['post'],
                        post,
                        match['score']
                    )

                    # Notify the matching post owner
                    self.matching_service.create_match_notification(
                        match['post'].user_id,
                        post,
                        match['post'],
                        match['score']
                    )
            else:
                print("No matches found")  # Debug log

        except Exception as e:
            print(f"Error processing matches: {e}")
            logging.error(f"Error processing matches: {e}")
