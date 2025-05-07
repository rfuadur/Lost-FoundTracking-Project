from app.models.post import Post
from app import db
from sqlalchemy import or_, and_
from datetime import datetime

class PostRepository:
    def get_by_type(self, type_name):
        return Post.query.filter_by(type=type_name).order_by(Post.post_date.desc()).all()
        
    def get_by_id(self, post_id):
        return Post.query.get_or_404(post_id)
        
    def create(self, data):
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return post
        
    def update(self, post):
        db.session.commit()
        return post
        
    def delete(self, post):
        db.session.delete(post)
        db.session.commit()
        
    def get_by_user_id(self, user_id):
        return Post.query.filter_by(user_id=user_id).all()
    
    def get_recent(self, limit):
        return Post.query.order_by(Post.post_date.desc()).limit(limit).all()

    def get_by_type_and_user(self, type_name, user_id):
        return Post.query.filter_by(
            type=type_name,
            user_id=user_id
        ).order_by(Post.post_date.desc()).all()

    def search(self, query, filters=None):
        """
        Search posts with advanced filtering
        """
        search = f"%{query}%"
        base_query = Post.query.filter(
            or_(
                Post.item_name.ilike(search),
                Post.description.ilike(search),
                Post.category_name.ilike(search),
                Post.location.ilike(search)  # Add location to searchable fields
            )
        )
        
        if filters:
            if filters.get('type'):
                base_query = base_query.filter(Post.type == filters['type'])
                
            if filters.get('category'):
                base_query = base_query.filter(Post.category_name == filters['category'])
                
            if filters.get('location'):
                location_search = f"%{filters['location']}%"
                base_query = base_query.filter(Post.location.ilike(location_search))
                
            if filters.get('date_from'):
                try:
                    date_from = datetime.strptime(filters['date_from'], '%Y-%m-%d')
                    # Search against lOrF_date field instead of date
                    base_query = base_query.filter(Post.lOrF_date >= date_from)
                except ValueError:
                    pass
                
            if filters.get('date_to'):
                try:
                    date_to = datetime.strptime(filters['date_to'], '%Y-%m-%d')
                    # Search against lOrF_date field instead of date
                    base_query = base_query.filter(Post.lOrF_date <= date_to)
                except ValueError:
                    pass
        
        print("SQL Query:", str(base_query))  # Debug print
        results = base_query.order_by(Post.post_date.desc()).all()
        print("Results count:", len(results))  # Debug print
        return results