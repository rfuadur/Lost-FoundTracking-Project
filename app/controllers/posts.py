from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.services.post_service import PostService
from app.services.search_service import SearchService
from app.utils.decorators import login_required, user_only
from app.models.verificationClaim import VerificationClaim  # Fixed import path
from app.utils.image_utils import save_image  # Import save_image utility

posts_bp = Blueprint("posts", __name__)
post_service = PostService()
search_service = SearchService()


@posts_bp.route("/lost-items")
@login_required
def lost_items():
    items = post_service.get_all_lost_items()
    return render_template("lost_items.html", items=items)


@posts_bp.route("/found-items")
@login_required
def found_items():
    items = post_service.get_all_found_items()
    return render_template("found_items.html", items=items)


@posts_bp.route("/report-lost-item", methods=["GET", "POST"])
@login_required
def report_lost_item():
    if request.method == "POST":
        try:
            post = post_service.create_lost_item(
                request.form, request.files, session["user_id"]
            )
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
            post = post_service.create_found_item(
                request.form, request.files, session["user_id"]
            )
            flash("Found item reported successfully!", "success")
            return redirect(url_for("posts.found_items"))
        except Exception as e:
            flash(f"Error reporting found item: {str(e)}", "danger")
    return render_template("report_found_item.html")


@posts_bp.route("/post/<int:post_id>")
@login_required
def view_post(post_id):
    post = post_service.get_by_id(post_id)
    is_owner = session["user_id"] == post.user_id
    verification_claim = None

    if not is_owner:
        verification_claim = VerificationClaim.query.filter_by(
            post_id=post_id, user_id=session["user_id"]
        ).first()

    return render_template(
        "view_post.html",
        post=post,
        post_owner=post.user,
        is_owner=is_owner,
        verification_claim=verification_claim,
    )


@posts_bp.route("/user-posts")
@login_required
def user_posts():
    posts = post_service.get_by_user_id(session["user_id"])
    return render_template("user_posts.html", posts=posts)


@posts_bp.route("/my-lost-items")
@login_required
def my_lost_items():
    posts = post_service.get_by_type_and_user("lost", session["user_id"])
    return render_template("user_posts.html", posts=posts, type="lost")


@posts_bp.route("/my-found-items")
@login_required
def my_found_items():
    posts = post_service.get_by_type_and_user("found", session["user_id"])
    return render_template("user_posts.html", posts=posts, type="found")


@posts_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
@user_only
def edit_post(post_id):
    post = post_service.get_by_id(post_id)
    if session.get("user_id") != post.user_id:
        flash("Access denied", "danger")
        return redirect(url_for("posts.view_post", post_id=post.id))

    if request.method == "POST":
        try:
            post.description = request.form.get("description")
            post.category_name = request.form.get("category")
            post.location = request.form.get("location")

            if "images" in request.files:
                images = []
                for file in request.files.getlist("images"):
                    if file.filename:
                        filename = save_image(file)
                        if filename:
                            images.append(filename)
                if images:
                    post.images = ",".join(images)

            post_service.update(post)
            flash("Post updated successfully", "success")
            return redirect(url_for("posts.view_post", post_id=post.id))
        except Exception as e:
            flash(f"Error updating post: {str(e)}", "danger")

    return render_template("edit_post.html", post=post)


@posts_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
@user_only
def delete_post(post_id):
    post = post_service.get_by_id(post_id)
    if session.get("user_id") != post.user_id:
        flash("Access denied", "danger")
        return redirect(url_for("posts.view_post", post_id=post.id))

    post_service.delete(post)
    flash("Post deleted successfully", "success")
    return redirect(url_for("posts.user_posts"))


@posts_bp.route("/search")
@login_required 
def search():
    query = request.args.get('q', '').strip()
    
    # Collect all filters and clean them
    filters = {
        'type': request.args.get('type', '').strip(),
        'category': request.args.get('category', '').strip(),
        'location': request.args.get('location', '').strip(),
        'date_from': request.args.get('date_from', '').strip(),
        'date_to': request.args.get('date_to', '').strip()
    }
    
    # Check if we have any search criteria
    has_search = query or any(filters.values())
    if not has_search:
        flash("Please enter a keyword or select filters to search", "warning")
        return redirect(request.referrer or url_for('dashboard.dashboard'))
    
    # Remove empty filters
    filters = {k: v for k, v in filters.items() if v}
    
    # For debugging
    print("Search query:", query)
    print("Applied filters:", filters)
    
    results = search_service.search_posts(query, filters)
    return render_template('search_results.html', 
                         query=query,
                         results=results,
                         type=filters.get('type', ''),
                         category=filters.get('category', ''),
                         location=filters.get('location', ''),
                         date_from=filters.get('date_from', ''),
                         date_to=filters.get('date_to', ''))
