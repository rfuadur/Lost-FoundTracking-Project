from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.services.admin_service import AdminService
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)
admin_service = AdminService()
user_service = UserService()
post_service = PostService()

@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    stats = admin_service.get_dashboard_stats()
    recent_reports = admin_service.get_recent_reports()
    # recent_users = admin_service.get_recent_users()

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_reports=recent_reports)

@admin_bp.route("/users")
@admin_required
def manage_users():
    users = admin_service.get_all_users()  # Changed from user_service to admin_service
    return render_template('admin/users.html', users=users)

@admin_bp.route("/reports")
@admin_required
def manage_reports():
    fraud_reports = admin_service.get_recent_reports(limit=None)  # Get all reports
    return render_template('admin/manage_reports.html', fraud_reports=fraud_reports)

@admin_bp.route("/user/<int:user_id>/toggle-ban", methods=['POST'])
@admin_required
def toggle_user_ban(user_id):
    success = admin_service.toggle_user_ban(user_id)  # Use direct toggle method
    if success:
        flash("User ban status toggled successfully", "success")
    else:
        flash("Failed to update user ban status", "danger")
    return redirect(url_for('admin.manage_users'))

@admin_bp.route("/fraud-report/<int:report_id>/resolve", methods=['POST'])
@admin_required
def resolve_fraud_report(report_id):
    action = request.form.get('action')
    admin_service.resolve_report(report_id, action)
    flash("Fraud report resolved successfully", "success")
    return redirect(url_for('admin.manage_reports'))

@admin_bp.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@admin_required
def edit_post(post_id):
    if request.method == 'POST':
        try:
            post_data = {
                'item_name': request.form.get('item_name'),
                'description': request.form.get('description'),
                'category_name': request.form.get('category'),
                'location': request.form.get('location'),
                'contact_method': request.form.get('contact_method'),
                'type': request.form.get('type'),
                'lOrF_date': request.form.get('lost_found_date'),  # Fixed field name
                'images': request.files.getlist('images')
            }
            post = post_service.get_by_id(post_id)  # Get post first
            post_service.update(post, post_data)  # Use correct update method
            flash("Post updated successfully", "success")
            return redirect(url_for('admin.manage_posts'))
        except Exception as e:
            flash(f"Error updating post: {str(e)}", "danger")
    post = post_service.get_by_id(post_id)  # Use correct get method
    return render_template('admin/edit_post.html', post=post)

@admin_bp.route("/post/<int:post_id>/delete", methods=['POST'])
@admin_required
def delete_post(post_id):
    post = post_service.get_by_id(post_id)  # Get post first
    post_service.delete(post)  # Use correct delete method
    flash("Post deleted successfully", "success")
    return redirect(url_for('admin.manage_posts'))

@admin_bp.route("/posts")
@admin_required
def manage_posts():
    filters = {
        'category': request.args.get('category', ''),
        'type': request.args.get('type', ''),
        'date_from': request.args.get('date_from', ''),
        'date_to': request.args.get('date_to', ''),
        'location': request.args.get('location', '')
    }
    posts = post_service.search_posts("", filters)  # Changed to use proper search method
    return render_template('admin/manage_posts.html', posts=posts, filters=filters)
