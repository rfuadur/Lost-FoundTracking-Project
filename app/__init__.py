from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lostandfound.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev_secret_key"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, '..', 'static', 'uploads')
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

db = SQLAlchemy(app)

# Ensure uploads directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.context_processor
def inject_common_data():
    notifications = []  # You can implement actual notifications later
    notifications_count = len(notifications)
    return {
        'current_year': datetime.utcnow().year,
        'notifications': notifications,
        'notifications_count': notifications_count
    }

# Add root route handler
@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.dashboard"))

# Import controllers after db initialization to avoid circular imports
from app.controllers.auth import auth_bp
from app.controllers.dashboard import dashboard_bp
from app.controllers.posts import posts_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(posts_bp, url_prefix='/posts')

# Register error handlers
from app.utils.error_handlers import register_error_handlers
register_error_handlers(app)
