from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if user exists
    user = User.query.filter_by(email='user@fifa26.com').first()
    
    if user:
        user.set_password("password123")
        db.session.commit()
        print("✅ Password reset for existing user!")
    else:
        # Create new user
        new_user = User(
            username="Admin User",
            email="user@fifa26.com",
            country="Bangladesh",
            is_admin=True
        )
        new_user.set_password("password123")
        db.session.add(new_user)
        db.session.commit()
        print("✅ New test user created!")

    print("Email: user@fifa26.com")
    print("Password: password123")