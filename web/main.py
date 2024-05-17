from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
# from UserClasses.User import User
import logging
from UserClasses.User import User
from UserClasses.Manager import DatabaseHandler
from UserClasses.Manager import SessionManager
from UserClasses.Manager import TemplateRenderer
import json

logging.basicConfig(level=logging.INFO)  # Set logging level to INFO



app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'diiimooooooon'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'keycardapp'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():

    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        password = hashlib.sha1((password + app.secret_key).encode()).hexdigest()

        dh = DatabaseHandler(mysql)

        # # Fetch one record and return result
        account = dh.get_user_by_username_and_password(username, password)
        # Check if account exists using MySQL
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            # Fetch cards associated with this account
            cards = dh.get_card_by_account_id(account['id'])

            # Log the fetched cards in the console
            logging.info("Cards associated with user %s: %s", username, cards)
            # Store cards in session for later use
            session['cards'] = cards



            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    
    print("cards")

    return render_template('index.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   SessionManager.logout()
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/pythonlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    dh = DatabaseHandler(mysql)
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        account = dh.get_account_data_by_username(username)
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            dh.insert_data_in_account(username, password, email)
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)






# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/pythonlogin/home')
def home():
    # Check if the user is logged in
    if SessionManager.is_logged_in():
        dh = DatabaseHandler(mysql)
        # User is loggedin show them the home page
        account = dh.get_account_data_by_id(session['id'])
        cards = dh.get_card_by_account_id(account['id'])
        return render_template('home.html', username=session['username'],  account=account, cards=cards)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/pythonlogin/profile')
def profile():
    # Check if the user is logged in
    if SessionManager.is_logged_in():
        dh = DatabaseHandler(mysql)
        # We need all the account info for the user so we can display it on the profile page
        account = dh.get_account_data_by_id(session['id'])
        cards = dh.get_card_by_account_id(account['id'])
        # Show the profile page with account info
        return render_template('profile.html', account=account, cards=cards)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/card/<int:card_id>')
def card(card_id):
    dh = DatabaseHandler(mysql)
    # Fetch the card details from the database based on its ID
    card = dh.get_card_by_id(card_id)
    # Render the card page template with the card details
    return render_template('card.html', card=card)


@app.route('/pythonlogin/scan')
def scan():
    return render_template('scan.html')

@app.route('/process_qr_code', methods=['POST'])
def process_qr_code():
    # Get the JSON data from the request
    data = request.json
    qr_data = data['qr_data']
    print(qr_data)
    data = json.loads(qr_data)
    # print(data)
    # print(data['key'])
    # print(data['company'])
    # Get the current user's ID from the session
    user_id = session.get('id')

    # Ensure user is logged in
    if user_id is None:
        return jsonify({'error': 'User not logged in'}), 401

    # Extract card information from the JSON data
    card_key = data['key']
    # print(type(card_key))
    # print(card_key)
    card_company = data['company']

    # Ensure the required fields are present
    if not card_key or not card_company:
        return jsonify({'error': 'Missing key or company in QR data'}), 400

    # Default image path
    img_path = 'default_path'

    try:
        # Insert the card into the database for the current user
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO cards (`key`, company, imp_path, account_id) VALUES (%s, %s, %s, %s)",
            (card_key, card_company, img_path, user_id)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'redirect_url': url_for('card_added')}), 200
        # return render_template('card_added.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/card_added')
def card_added():
        return render_template('card_added.html')