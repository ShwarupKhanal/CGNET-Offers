from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cgusers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CGUsers(db.Model):
    __tablename__ = 'cgusers'  
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

def generate_offers(user):
    discount_offers = []
    bonus_offers = []
    
    print(f"DEBUG: Inside generate_offers: PlanType={user.PlanType}, Bandwidth={user.Bandwidth}, Month={user.Month}")

    if user.PlanType.lower() == "internet only":
        print("DEBUG: Matching PlanType as Internet Only")
        if user.Bandwidth in ["50", "70", "80", "101"]:
            print(f"DEBUG: Bandwidth {user.Bandwidth} matched")
            if user.Month == 1:
                print("DEBUG: Month is 1")
                discount_offers.append("Rs.2120 - 3Month 101Mbps Internet Plan")
                bonus_offers.append("At just Rs.2670 get 101Mbps - 3Month Internet + 1Month Bonus")
            elif user.Month == 3:
                print("DEBUG: Month is 3")
                discount_offers.append("Rs.9000 - 150Mbps - 3Month Internet Plan")
                bonus_offers.append("At just Rs.3220 get 150Mbps - 3Month Internet + 1Month Bonus")
    else:
        print(f"DEBUG: PlanType '{user.PlanType}' did not match 'Internet Only'")

    if user.PlanType.lower() == "internet+iptv":
        print("DEBUG: Matching PlanType as Internet+IPTV")
        if user.Bandwidth in ["57", "77"]:
            if user.Month in [3, 12]:
                print("DEBUG: Matching Bandwidth and Month for Internet+IPTV")
                discount_offers.append("Rs.9578 - 77Mbps - 12Month Internet+IPTV Plan")
                bonus_offers.append("At just Rs.11117 get 77Mbps - 12Month Internet + 1Month Bonus")
        if user.Bandwidth in ["111", "157"]:
            if user.Month in [3, 12]:
                print("DEBUG: Matching Bandwidth and Month for Internet+IPTV")
                discount_offers.append("Rs.12270 - 150Mbps - 12Month Internet+IPTV Plan")
                bonus_offers.append("At just Rs.14023 get 157Mbps - 12Month Internet + 1Month Bonus")

    return discount_offers, bonus_offers


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
        print(f"Found user: {user.CustomerName}, PlanType: {user.PlanType}, Bandwidth: {user.Bandwidth}, Month: {user.Month}")
        discount_offers, bonus_offers = generate_offers(user)

        return jsonify({
            "discountOffers": discount_offers,
            "bonusOffers": bonus_offers
        })
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

w
