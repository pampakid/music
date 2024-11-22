# backend/test_db.py
from app import create_app, db
from app.models.user import User

def test_connection():
    app = create_app()
    with app.app_context():
        try:
            # Test database connection
            db.create_all()
            print("✅ Database connection successful!")
            print("✅ Tables created successfully!")
            
            # Test creating a user
            test_user = User(
                username="test",
                email="test@example.com"
            )
            test_user.set_password("test123")
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully!")
            
            # Clean up
            db.session.delete(test_user)
            db.session.commit()
            print("✅ Test cleanup successful!")
            
        except Exception as e:
            print("❌ Error:", str(e))
            return False
    return True

if __name__ == "__main__":
    test_connection()