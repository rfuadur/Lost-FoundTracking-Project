from app import app, db, socketio
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_default_users():
    if not User.query.filter_by(email="admin@test.com").first():
        admin = User(
            name="Admin User",
            email="admin@test.com",
            password=generate_password_hash("admin123"),
            is_admin=True,
            contact_info="Admin Contact"
        )
        db.session.add(admin)

    if not User.query.filter_by(email="user@test.com").first():
        user = User(
            name="Test User",
            email="user@test.com",
            password=generate_password_hash("user123"),
            is_admin=False,
            contact_info="Test User Contact"
        )
        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_users()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
