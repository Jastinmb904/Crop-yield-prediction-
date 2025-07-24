from app import app, db, User

# Query all users
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, email: {user.email}, Password: {user.password}")  # Passwords are hashed