# Import necessary modules
from app import app, db

# Create the Flask application context
with app.app_context():
    # Create the database tables
    db.create_all()
