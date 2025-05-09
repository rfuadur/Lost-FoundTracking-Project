from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from app.services.dashboard_service import DashboardService
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.notification_service import NotificationService
from app.services.verification_service import VerificationService
from app.utils.decorators import login_required

dashboard_bp = Blueprint("dashboard", __name__)

# Initialize services
dashboard_service = DashboardService()
user_service = UserService()
post_service = PostService()
notification_service = NotificationService()
verification_service = VerificationService()

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    current_user = user_service.get_by_id(session['user_id'])
    stats = post_service.get_user_stats(session['user_id'])
    recent_activities = dashboard_service.get_recent_activities()
    pending_claims_count = notification_service.get_pending_claims_count(session['user_id'])
    top_contributors = dashboard_service.get_top_contributors()
    return render_template(
        "dashboard.html",
        user=current_user,
        user_posts_count=stats["total_posts"],
        lost_items_count=stats["lost_items"],
        found_items_count=stats["found_items"],
        recent_activities=recent_activities,
        pending_claims_count=pending_claims_count,
        top_contributors=top_contributors,
    )


@dashboard_bp.route("/notifications/mark-read/<int:notification_id>")
@login_required
def mark_notification_read(notification_id):
    notification = notification_service.mark_as_read(notification_id, session['user_id'])
    if notification:
        return redirect(notification.link)
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/notifications/clear-all")
@login_required
def clear_notifications():
    notification_service.clear_all_notifications(session['user_id'])
    return redirect(request.referrer or url_for('dashboard.dashboard'))

@dashboard_bp.route("/notifications")
@login_required
def notifications():
    notifications = notification_service.get_user_notifications(session['user_id'])
    return render_template('notifications.html', notifications=notifications)

@dashboard_bp.route("/notifications/mark-all-read")
@login_required
def mark_all_notifications_read():
    notification_service.mark_all_read(session['user_id'])
    flash('All notifications marked as read', 'success')
    return redirect(url_for('dashboard.notifications'))

@dashboard_bp.route("/notifications/delete/<int:notification_id>")
@login_required
def delete_notification(notification_id):
    if notification_service.delete_notification(notification_id, session['user_id']):
        flash('Notification deleted', 'success')
    else:
        flash('Error deleting notification', 'danger')
    return redirect(url_for('dashboard.notifications'))

@dashboard_bp.route("/all-claims")
@login_required
def all_claims():
    claims_data = verification_service.get_user_claims(session['user_id'])
    return render_template('all_claims.html', claims=claims_data)
