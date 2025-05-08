from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.services.verification_service import VerificationService
from app.services.notification_service import NotificationService
from app.utils.decorators import login_required

verification_bp = Blueprint('verification', __name__)
verification_service = VerificationService()
notification_service = NotificationService()

@verification_bp.route("/post/<int:post_id>/verify", methods=["GET", "POST"])
@login_required
def verify_item(post_id):
    if request.method == "POST":
        try:
            verification_service.create_verification_claim(
                post_id,
                session['user_id'],
                request.form,
                request.files
            )
            post = verification_service.get_post(post_id)

            # Notify post owner about new claim
            notification_service.create_verification_notification(
                post.user_id,
                f"New verification claim received for your item '{post.item_name}'",
                url_for('verification.view_claims', post_id=post_id)
            )

            flash("Your verification claim has been submitted successfully.", "success")
            return redirect(url_for('posts.view_post', post_id=post_id))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for('verification.verify_item', post_id=post_id))

    post = verification_service.get_post(post_id)
    return render_template('verify_item.html', post=post)

@verification_bp.route("/post/<int:post_id>/claims")
@login_required
def view_claims(post_id):
    post = verification_service.get_post(post_id)
    if session.get("user_id") != post.user_id:
        flash("Access denied", "danger")
        return redirect(url_for("posts.view_post", post_id=post_id))

    claims = verification_service.get_post_claims(post_id)
    return render_template("view_claims.html", post=post, claims=claims)

@verification_bp.route("/post/<int:post_id>/claim/<int:claim_id>/update", methods=["POST"])
@login_required
def update_claim_status(post_id, claim_id):
    post = verification_service.get_post(post_id)
    if session.get("user_id") != post.user_id:
        flash("Access denied", "danger")
        return redirect(url_for("posts.view_post", post_id=post_id))

    new_status = request.form.get("status")
    if new_status in ["approved", "rejected"]:
        result = verification_service.update_claim_status(claim_id, post_id, new_status)
        if result:
            if new_status == "approved" and isinstance(result, dict):
                notification_service.create_chat_enabled_notifications(
                    result['claim_user_id'],
                    result['post_user_id'],
                    result['post_id'],
                    result['post_name']
                )
            flash(f"Claim has been {new_status}", "success")
        else:
            flash("Error updating claim status", "danger")

    return redirect(url_for("verification.view_claims", post_id=post_id))
