from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from app.utils.time_utils import utc_now
import logging
import os

load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///lostandfound.db")
# Fix for some postgres hosting providers requiring sslmode to require
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    if debug_mode:
        secret_key = "dev_secret_key"
        logging.warning("SECRET_KEY not set; using an insecure default for local development only.")
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable must be set. "
            "For local development, set FLASK_DEBUG=true to allow an insecure default."
        )
app.config["SECRET_KEY"] = secret_key

app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, '..', 'static', 'uploads')
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Mail Configuration (Mailjet Send API)
app.config['MAILJET_API_KEY'] = os.environ.get('MAILJET_API_KEY')
app.config['MAILJET_SECRET_KEY'] = os.environ.get('MAILJET_SECRET_KEY')
app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER')
app.config['MAIL_SENDER_NAME'] = os.environ.get('MAIL_SENDER_NAME', 'Lost & Found')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, async_mode='eventlet')
csrf = CSRFProtect(app)

# Ensure uploads directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.context_processor
def inject_common_data():
    from app.models.notification import Notification
    from app.models.chat import Chat
    notifications = []
    notifications_count = 0
    unread_chats = 0

    if 'user_id' in session:
        # Get all notifications, ordered by created_at
        notifications = Notification.query.filter_by(
            user_id=session['user_id']
        ).order_by(Notification.created_at.desc()).all()

        # Count only unread notifications
        notifications_count = Notification.query.filter_by(
            user_id=session['user_id'],
            is_read=False
        ).count()

        # Count unread chats
        unread_chats = Chat.query.filter_by(
            receiver_id=session['user_id'],
            is_read=False
        ).count()

    return {
        'current_year': utc_now().year,
        'notifications': notifications,
        'notifications_count': notifications_count,
        'unread_chats': unread_chats
    }


# Add root route handler
@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.dashboard"))

# Import controllers after db initialization to avoid circular imports
from app.controllers.auth import auth_bp
from app.controllers.posts import posts_bp
from app.controllers.dashboard import dashboard_bp
from app.controllers.verification import verification_bp
from app.controllers.admin import admin_bp
from app.controllers.chat import chat_bp
from app.controllers.reports import reports_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(verification_bp, url_prefix='/verification')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(reports_bp, url_prefix='/reports')

# Import socket events after socketio initialization
from app.sockets import socket_events

# Register error handlers
from app.utils.error_handlers import register_error_handlers
register_error_handlers(app)
