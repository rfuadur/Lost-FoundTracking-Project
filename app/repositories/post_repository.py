from app.models.post import Post
from app import db
from sqlalchemy import or_

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

    def search(self, query, post_type=None):
        """
        Search posts based on keyword and optional type filter
        """
        search = f"%{query}%"
        base_query = Post.query.filter(
            or_(
                Post.item_name.ilike(search),
                Post.description.ilike(search),
                Post.category_name.ilike(search)
            )
        )

        if post_type:
            base_query = base_query.filter(Post.type == post_type)

        return base_query.order_by(Post.post_date.desc()).all()
