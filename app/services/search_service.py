from app.repositories.post_repository import PostRepository

class SearchService:
    def __init__(self):
        self.post_repository = PostRepository()

    def search_posts(self, query, post_type=None):
        """
        Search posts based on keyword and optional type filter
        """
        return self.post_repository.search(query, post_type)
