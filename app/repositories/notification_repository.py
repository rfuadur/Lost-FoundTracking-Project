from app.models.notification import Notification
from app import db

class NotificationRepository:
    def get_by_id(self, notification_id):
        """Get notification by ID"""
        return Notification.query.get(notification_id)

    def get_user_notifications(self, user_id, limit=None):
        """Get notifications for a user"""
        query = Notification.query.filter_by(user_id=user_id)
        if limit:
            query = query.limit(limit)
        return query.all()

    def create(self, data):
        """Create a new notification"""
        notification = Notification(**data)
        db.session.add(notification)
        db.session.commit()
        return notification

    def mark_as_read(self, notification_id):
        """Mark notification as read"""
        notification = self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
        return notification

    def delete_user_notifications(self, user_id):
        """Delete all notifications for a user"""
        Notification.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def save_all(self):
        """Save all changes to the database"""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving changes: {e}")
            return False

    def delete(self, notification):
        """Delete a specific notification"""
        try:
            db.session.delete(notification)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting notification: {e}")
            return False

    def mark_all_read(self, user_id):
        """Mark all notifications as read for a user"""
        try:
            notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
            for notification in notifications:
                notification.is_read = True
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error marking all notifications as read: {e}")
            return False
