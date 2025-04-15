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
