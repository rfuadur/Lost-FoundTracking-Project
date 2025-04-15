from app.models.post import Post
from app import db

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