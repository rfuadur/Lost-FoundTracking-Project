from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.notification_repository import NotificationRepository

class DashboardService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.post_repository = PostRepository()
        self.notification_repository = NotificationRepository()

    def get_user_stats(self, user_id):
        return {
            'total_posts': self.post_repository.count_user_posts(user_id),
            'lost_items': self.post_repository.count_user_posts(user_id, 'lost'),
            'found_items': self.post_repository.count_user_posts(user_id, 'found')
        }

    def get_recent_activities(self, limit=6):
        return self.post_repository.get_recent(limit)
    
    def get_top_contributors(self, limit=5):
        return self.user_repository.get_top_contributors(limit)
    