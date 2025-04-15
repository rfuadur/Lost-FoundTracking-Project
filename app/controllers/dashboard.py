from flask import Blueprint, render_template, session
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__)
user_service = UserService()
post_service = PostService()

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    current_user = user_service.get_by_id(session['user_id'])
    stats = post_service.get_user_stats(session['user_id'])
    recent_activities = post_service.get_recent_activities()
    
    return render_template(
        "dashboard.html",
        user=current_user,
        user_posts_count=stats['total_posts'],
        lost_items_count=stats['lost_items'],
        found_items_count=stats['found_items'],
        recent_activities=recent_activities
    )
