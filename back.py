from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cgoffers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CGUsers(db.Model):
    __tablename__ = 'cgoffers'  
    AccountID = db.Column(db.String(255), primary_key=True)
    UserID = db.Column(db.String(80), unique=True, nullable=False)
    CustomerName = db.Column(db.String(120), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    Plan = db.Column(db.String(100), nullable=False)
    ServiceExpiryDate = db.Column(db.Date, nullable=True)
    Bandwidth = db.Column(db.String(10), nullable=True)
    Month = db.Column(db.Integer, nullable=True)
    PlanType = db.Column(db.String(50), nullable=True)
    Offer1 = db.Column(db.String(255), nullable=True)
    Offer2 = db.Column(db.String(255), nullable=True)

def generate_offers(user):
    offer1 = user.Offer1 if user.Offer1 else []
    offer2 = user.Offer2 if user.Offer2 else []

    return offer1, offer2

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/offers', methods=['GET'])
def offers():
    search_input = request.args.get('search', '').strip()

    if not search_input:
        return jsonify({"error": "No input provided"}), 400

    user = None

    if search_input.isdigit() and len(search_input) == 10:
        user = CGUsers.query.filter_by(Phone=search_input).first()
    elif search_input.startswith('H') and search_input[1:].isdigit():
        user = CGUsers.query.filter_by(AccountID=search_input).first()
    else:
        user = CGUsers.query.filter_by(UserID=search_input).first()

    if user:
        print(f"Found user: {user.CustomerName}, Offer1: {user.Offer1}, Offer2: {user.Offer2}")
        offer1, offer2 = generate_offers(user)
        return jsonify({
            "offer1": offer1,
            "offer2": offer2
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


