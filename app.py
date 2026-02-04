from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from google.cloud import firestore
from flask_cors import CORS
import os

# Set path to Google Cloud service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app)

# Firestore client
db = firestore.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        db.collection('users').document(email).set({
            'fullname': fullname,
            'email': email,
            'password': password  # 🔒 You should hash passwords in production
        })
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        user_doc = db.collection('users').document(email).get()
        if user_doc.exists and user_doc.to_dict()['password'] == password:
            session['user'] = {
                'uid': email,
                'email': email,
                'name': user_doc.to_dict().get('fullname', 'No Name'),
                'is_guest': False
            }
            return redirect(url_for('home'))
        else:
            return "Invalid credentials."

    return render_template('login.html')

@app.route('/firebase-login', methods=['POST'])
def firebase_login():
    data = request.get_json()
    session['user'] = {
        'uid': data['uid'],
        'email': data['email'],
        'name': data['name'],
        'is_guest': data['is_guest']
    }
    return jsonify({ 'message': 'User session stored successfully' }), 200

@app.route('/guest-login', methods=['POST'])
def guest_login():
    session['user'] = {
        'uid': 'guest',
        'email': 'guest@guest.com',
        'name': 'Guest User',
        'is_guest': True
    }
    return redirect(url_for('home'))

@app.route('/home')
def home():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template("home.html", user=user)

@app.route('/find')
def find():
    return "Find Page Placeholder"

@app.route('/about')
def about():
    return "About Page Placeholder"

if __name__ == '__main__':
    app.run(debug=True)