from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.services.post_service import PostService
from app.utils.decorators import login_required, user_only

posts_bp = Blueprint('posts', __name__)
post_service = PostService()


@posts_bp.route("/report-lost-item", methods=["GET", "POST"])
@login_required
def report_lost_item():
    if request.method == "POST":
        try:
            post = post_service.create_lost_item(request.form, request.files, session["user_id"])
            flash("Lost item reported successfully!", "success")
            return redirect(url_for("posts.lost_items"))
        except Exception as e:
            flash(f"Error reporting lost item: {str(e)}", "danger")
    return render_template("report_lost_item.html")

@posts_bp.route("/report-found-item", methods=["GET", "POST"])
@login_required
def report_found_item():
    if request.method == "POST":
        try:
            post = post_service.create_found_item(request.form, request.files, session["user_id"])
            flash("Found item reported successfully!", "success")
            return redirect(url_for("posts.found_items"))
        except Exception as e:
            flash(f"Error reporting found item: {str(e)}", "danger")
    return render_template("report_found_item.html")

