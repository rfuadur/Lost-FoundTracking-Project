from app.repositories.notification_repository import NotificationRepository
from app.repositories.verification_repository import VerificationRepository

class NotificationService:
    def __init__(self):
        self.notification_repository = NotificationRepository()
        self.verification_repository = VerificationRepository()

    def mark_as_read(self, notification_id, user_id):
        """Mark a notification as read if it belongs to the user"""
        notification = self.notification_repository.get_by_id(notification_id)
        if notification and notification.user_id == user_id:
            return self.notification_repository.mark_as_read(notification_id)
        return None

    def mark_all_read(self, user_id):
        """Mark all notifications as read for a user"""
        return self.notification_repository.mark_all_read(user_id)

    def delete_notification(self, notification_id, user_id):
        """Delete a specific notification"""
        notification = self.notification_repository.get_by_id(notification_id)
        if notification and notification.user_id == user_id:
            return self.notification_repository.delete(notification)
        return False

    def clear_all_notifications(self, user_id):
        """Delete all notifications for a user"""
        try:
            self.notification_repository.delete_user_notifications(user_id)
            return True
        except Exception as e:
            print(f"Error clearing notifications: {e}")
            return False

    def get_user_notifications(self, user_id, limit=None):
        """Get all notifications for a user"""
        return self.notification_repository.get_user_notifications(user_id, limit)

    def create_verification_notification(self, user_id, message, link):
        """Create a new verification-related notification"""
        try:
            data = {
                'user_id': user_id,
                'title': "Verification Update",
                'message': message,
                'link': link,
                'is_read': False
            }
            return self.notification_repository.create(data)
        except Exception as e:
            print(f"Error creating verification notification: {e}")
            return None

    def get_pending_claims_count(self, user_id):
        """Get count of unread verification claims for a user"""
        return self.verification_repository.get_pending_claims_count(user_id)

    def create_chat_enabled_notifications(self, claimer_id, owner_id, post_id, item_name):
        """Create notifications for both users when chat is enabled"""
        try:
            # Notify claimer
            self.notification_repository.create({
                'user_id': claimer_id,
                'title': 'Claim Approved',
                'message': f'Your claim for "{item_name}" has been approved. You can now chat with the owner.',
                'link': f'/chat/conversation/{post_id}',
                'is_read': False
            })

            # Notify owner
            self.notification_repository.create({
                'user_id': owner_id,
                'title': 'Chat Enabled',
                'message': f'You can now chat with the claimer of "{item_name}".',
                'link': f'/chat/conversation/{post_id}',
                'is_read': False
            })
            return True
        except Exception as e:
            print(f"Error creating chat notifications: {e}")
            return False
