from app.repositories.post_repository import PostRepository

class SearchService:
    def __init__(self):
        self.post_repository = PostRepository()

    def search_posts(self, query, filters=None):
        """
        Search posts based on keyword and filters

        Args:
            query (str): Search keyword
            filters (dict): Optional filters containing:
                - type: post type (lost/found)
                - category: item category
                - date_from: start date
                - date_to: end date
                - location: location keyword
        """
        return self.post_repository.search(query, filters)
