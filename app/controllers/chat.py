from flask import Blueprint, render_template, session, jsonify, flash, redirect, url_for
from app.services.verification_service import VerificationService
from app.services.chat_service import ChatService
from app.services.post_service import PostService
from app.services.user_service import UserService
from app.utils.decorators import login_required

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# Initialize services
chat_service = ChatService()
post_service = PostService()
user_service = UserService()
verification_service = VerificationService()

@chat_bp.route('/inbox')
@login_required
def inbox():
    inbox_items = chat_service.get_inbox_items(session['user_id'])
    return render_template('chat/inbox.html',
                         owned_posts=inbox_items['owned_posts'],
                         other_posts=inbox_items['other_posts'])

@chat_bp.route('/conversation/<int:post_id>')
@login_required
def conversation(post_id):
    if not chat_service.can_access_chat(session['user_id'], post_id):
        return jsonify({'error': 'Unauthorized access'}), 403

    post = post_service.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    chats = chat_service.get_post_chats(post_id, session['user_id'])

    # Get chat participant info
    if post.user_id == session['user_id']:
        # If owner, get the approved claimer for found items
        if post.type == 'found':
            claim_data = verification_service.get_approved_claim(post_id)
            if claim_data:
                other_user = claim_data['user']
            else:
                flash('No approved claim found for this post', 'error')
                return redirect(url_for('posts.view_post', post_id=post_id))
        else:
            # For lost items, get first chatter
            other_chatter = next((chat for chat in chats if chat.sender_id != session['user_id']), None)
            other_user = user_service.get_by_id(other_chatter.sender_id) if other_chatter else None
    else:
        # If not owner, other user is the post owner
        other_user = user_service.get_by_id(post.user_id)

    if not other_user:
        flash('Could not determine chat participant', 'error')
        return redirect(url_for('posts.view_post', post_id=post_id))

    # Mark messages as read
    chat_service.mark_messages_read(post_id, session['user_id'])

    return render_template('chat/conversation.html',
                         post=post,
                         chats=chats,
                         other_user=other_user)
