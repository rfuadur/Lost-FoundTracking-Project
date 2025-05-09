from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.report_repository import ReportRepository
from datetime import datetime

class AdminService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.post_repository = PostRepository()
        self.report_repository = ReportRepository()

    def get_dashboard_stats(self):
        return {
            'total_users': self.user_repository.count_all(),
            'active_users': self.user_repository.count_active(),
            'admin_users': self.user_repository.count_admins(),
            'total_posts': self.post_repository.count_all(),
            'pending_reports': self.report_repository.count_by_status('pending'),
            'total_reports': self.report_repository.count_all()
        }

    def get_recent_reports(self, limit=5):
        return self.report_repository.get_recent(limit)

    def get_recent_users(self, limit=5):
        return self.user_repository.get_recent(limit)

    def toggle_user_ban(self, user_id):
        """Toggle user ban status independently of reports"""
        return self.user_repository.toggle_ban_status(user_id)

    def resolve_report(self, report_id, action):
        """Handle report resolution with different actions"""
        if not report_id:  # Direct user ban without report
            return False

        report = self.report_repository.get_by_id(report_id)
        if not report:
            return False

        report_data = {
            'status': 'resolved' if action == 'ban_user' else 'dismissed' if action == 'dismiss' else 'pending',
            'resolved_at': datetime.utcnow() if action != 'undo' else None
        }

        success = self.report_repository.update(report_id, report_data)
        if success and action == 'ban_user':
            self.user_repository.update_ban_status(report.reported_user_id, True)
        elif success and action == 'undo':
            self.user_repository.update_ban_status(report.reported_user_id, False)

        return success

    def get_all_users(self):
        return self.user_repository.get_all()
