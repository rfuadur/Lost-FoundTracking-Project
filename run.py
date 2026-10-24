import os
from app import app, db, socketio
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_default_users():
    """Seed demo accounts for local development only.

    Guarded by SEED_DEMO_USERS so production deployments never end up
    with a well-known admin/admin123 login. Set SEED_DEMO_USERS=true
    (and optionally DEMO_ADMIN_PASSWORD / DEMO_USER_PASSWORD) locally.
    """
    if os.environ.get("SEED_DEMO_USERS", "false").lower() != "true":
        return

    admin_password = os.environ.get("DEMO_ADMIN_PASSWORD", "admin123")
    user_password = os.environ.get("DEMO_USER_PASSWORD", "user123")

    if not User.query.filter_by(email="admin@test.com").first():
        admin = User(
            name="Admin User",
            email="admin@test.com",
            password=generate_password_hash(admin_password),
            is_admin=True,
            contact_info="Admin Contact"
        )
        db.session.add(admin)

    if not User.query.filter_by(email="user@test.com").first():
        user = User(
            name="Test User",
            email="user@test.com",
            password=generate_password_hash(user_password),
            is_admin=False,
            contact_info="Test User Contact"
        )
        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_users()
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    # Local development server only; production runs under gunicorn (see render.yaml)
    socketio.run(app, host="0.0.0.0", port=5000, debug=debug_mode, allow_unsafe_werkzeug=True)
