from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/testcg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model with the correct table name
class User(db.Model):
    __tablename__ = 'testcg'  # Specify the table name as 'testcg'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    plans = db.Column(db.String(50), nullable=False)

# API route to fetch offers
@app.route('/offers/<username>')
def get_offers(username):
    try:
        user = User.query.filter_by(username=username).first()  # Query based on username
        if user:
            # Offer plans based on the user's current plan
            offers = []
            if user.plans == "70mbps":
                offers = ["Upgrade to 101mbps @9000", "Upgrade to 150mbps @10000"]
            elif user.plans == "101mbps":
                offers = ["Upgrade to 150mbps @10000", "Upgrade to 250mbps @12000"]
            elif user.plans == "150mbps":
                offers = ["Upgrade to 250mbps @12000"]
            elif user.plans == "250mbps":
                offers = ["Get a free router with upgrade"]
            
            return jsonify({"offers": offers})
        else:
            return jsonify({"error": "User not found"})
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"})

# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('front.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
