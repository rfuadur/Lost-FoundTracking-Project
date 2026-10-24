from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from app.services.auth_service import AuthService
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
        
    if request.method == "POST":
        try:
            user = auth_service.authenticate(
                request.form.get("email"),
                request.form.get("password")
            )
            if user:
                auth_service.login_user(user)
                flash(f"Welcome back, {user.name}!", "success")
                return redirect(url_for("dashboard.dashboard"))
            flash("Invalid email or password", "danger")
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
        
    if request.method == "POST":
        try:
            user = auth_service.register(
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("password"),
                request.form.get("contact_info")
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("register.html")

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
        
    if request.method == "POST":
        email = request.form.get("email")
        # Always flash the same message for security, whether email exists or not
        auth_service.send_reset_email(email)
        flash("If an account with that email exists, a password reset link has been sent.", "info")
        return redirect(url_for("auth.login"))
        
    return render_template("forgot_password.html")

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
        
    # Verify token validity first
    email = auth_service.verify_reset_token(token)
    if not email:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("reset_password.html", token=token)
            
        try:
            auth_service.reset_password(token, password)
            flash("Your password has been updated! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("auth.login"))
            
    return render_template("reset_password.html", token=token)

@auth_bp.route("/logout")
@login_required
def logout():
    user_name = session.get("user_name", "User")
    auth_service.logout_user()
    flash(f"Goodbye, {user_name}! You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/home")
def root():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.dashboard"))

@auth_bp.route("/")  # Should be /auth/ in full URL
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login")) 
    return redirect(url_for("dashboard.dashboard"))
