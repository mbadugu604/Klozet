from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Define the base directory of your application
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'klozet.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To suppress a warning

db = SQLAlchemy(app)

# --- Database Models ---
# These define the structure of your tables in klozet.db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # You'll add more user-related fields later if needed

    def __repr__(self):
        return f'<User {self.username}>'

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False) # e.g., "Top", "Bottom", "Dress"
    color = db.Column(db.String(50), nullable=False)     # e.g., "Blue", "Red", "Black"
    # Add other attributes from your data strategy here:
    pattern = db.Column(db.String(50), nullable=True)    # e.g., "Solid", "Striped", "Floral"
    material = db.Column(db.String(50), nullable=True)   # e.g., "Cotton", "Denim"
    occasion = db.Column(db.String(50), nullable=True)   # e.g., "Casual", "Formal", "Party"
    season = db.Column(db.String(50), nullable=True)     # e.g., "Summer", "Winter", "All-Season"
    fit = db.Column(db.String(50), nullable=True)        # e.g., "Loose", "Fitted"
    image_url = db.Column(db.String(255), nullable=True) # Will store Cloudinary URL later
    last_worn_date = db.Column(db.Date, nullable=True)   # To track usage

    def __repr__(self):
        return f'<ClothingItem {self.item_type} ({self.color}) by User {self.user_id}>'

# --- Flask Routes ---
@app.route('/')
def hello_klozet():
    return "Hello, Klozet.!"

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Klozet. backend is running!"})

# --- Main execution block ---
if __name__ == '__main__':
    # This block runs when you execute app.py directly
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        print("Database tables created or already exist.")
    app.run(debug=True) # Run the Flask development server