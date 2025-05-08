from app.repositories.chat_repository import ChatRepository
from app.repositories.verification_repository import VerificationRepository
from app.repositories.post_repository import PostRepository

class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.verification_repository = VerificationRepository()
        self.post_repository = PostRepository()

    def get_post_chats(self, post_id, user_id):
        return self.chat_repository.get_post_chats(post_id, user_id)

    def get_inbox_items(self, user_id):
        posts = self.chat_repository.get_posts_with_chats(user_id)
        owned_posts = []
        other_posts = []

        for post in posts:
            if post.user_id == user_id:
                owned_posts.append(post)
            else:
                other_posts.append(post)

        return {
            'owned_posts': owned_posts,
            'other_posts': other_posts
        }

    def can_access_chat(self, user_id, post_id):
        post = self.post_repository.get_by_id(post_id)
        if not post:
            return False

        # For lost items, anyone can chat
        if post.type == 'lost':
            return True

        # Post owner can always chat
        if post.user_id == user_id:
            return True


        # For found items, only approved claimers can chat
        if post.type == 'found':
            claim = self.verification_repository.get_claim_by_status(
                post_id=post_id,
                user_id=user_id,
                status='approved'
            )
            return claim is not None

        return False

    def get_unread_count(self, user_id):
        return self.chat_repository.get_unread_messages_count(user_id)

    def mark_messages_read(self, post_id, user_id):
        return self.chat_repository.mark_messages_read(post_id, user_id)

    def create_message(self, post_id, sender_id, receiver_id, message_text):
        """Create a new chat message if user has access"""
        if not self.can_access_chat(sender_id, post_id):
            return None

        message = self.chat_repository.create_message(
            post_id=post_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_text=message_text
        )

        return {
            'id': message.id,
            'sender_id': message.sender_id,
            'message': message.message,
            'created_at': message.created_at.strftime('%H:%M')
        }

