import qrcode as qrcode
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_mysqldb import MySQL
import re, hashlib
# from UserClasses.User import User
import logging
from models.Manager import Factory
import json
from models.User import User
from models.Card import Card
# from flask_qrcode import QRcode
import qrcode
from io import BytesIO

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


# http://localhost:5000/keywallet/login - the following will be our login page, which will use both GET and POST requests
@app.route('/keywallet/login', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        user = User()

        user.input_username(username)
        user.input_password(password)

        password = Factory.use_password_manager().hash_password(user.get_password(), app.secret_key)

        user.input_hashed_password(password)

        # dh = DatabaseHandler(mysql)
        dh = Factory.create_database_handler(mysql)

        # # Fetch one record and return result
        account = dh.get_user_by_username_and_password(user.get_username(), user.get_hashed_password())

        # Check if account exists using MySQL
        if account:
            # Create session data, we can access this data in other routes
            user.input_email(account["email"])
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            # Fetch cards associated with this account
            cards = dh.get_card_by_account_id(account['id'])
            user.update_cards(cards)
            # Log the fetched cards in the console
            logging.info("Cards associated with user %s: %s", user.get_username(), user.get_cards())
            # Store cards in session for later use
            session['cards'] = user.get_cards()

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)

    print("cards")

    return render_template('index.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/keywallet/logout')
def logout():
    # Remove session data, this will log the user out
    Factory.use_session_manager().logout()
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/keywallet/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/keywallet/register', methods=['GET', 'POST'])
def register():
    # dh = DatabaseHandler(mysql)
    dh = Factory.create_database_handler(mysql)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User()
        user.input_username(username)
        user.input_password(password)
        user.input_email(email)
        # Check if account exists using MySQL
        account = dh.get_account_data_by_username(user.get_username())
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
            # hash = password + app.secret_key
            # hash = hashlib.sha1(hash.encode())
            # password = hash.hexdigest()
            password = Factory.use_password_manager().hash_password(user.get_password(), app.secret_key)
            user.input_hashed_password(password)
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            dh.insert_data_in_account(user.get_username(), user.get_hashed_password(), user.get_email())
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/keywallet/home')
def home():
    # Check if the user is logged in
    if Factory.use_session_manager().is_logged_in():
        # dh = DatabaseHandler(mysql)
        dh = Factory.create_database_handler(mysql)
        # User is loggedin show them the home page
        account = dh.get_account_data_by_id(session['id'])
        # print(account['email'])
        user = User()
        user.input_username(account['username'])
        user.input_password(account['password'])
        user.input_email(account['email'])
        cards = dh.get_card_by_account_id(account['id'])
        cards_instances = []
        for card in cards:
            next_card = Card()
            next_card.input_company_name(card["company"])
            next_card.input_key(card["key"])
            next_card.input_img_path(card["imp_path"])
            cards_instances.append(next_card)

        user.update_cards(cards)
        return render_template('home.html', username=user.get_username(), account=account, cards=user.get_cards())
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/keywallet/profile')
def profile():
    # Check if the user is logged in
    if Factory.use_session_manager().is_logged_in():
        # dh = DatabaseHandler(mysql)
        dh = Factory.create_database_handler(mysql)
        # We need all the account info for the user so we can display it on the profile page
        account = dh.get_account_data_by_id(session['id'])
        user = User()
        user.input_username(account['username'])
        user.input_password(account['password'])
        user.input_email(account['email'])
        cards = dh.get_card_by_account_id(account['id'])
        user.update_cards(cards)
        # Show the profile page with account info
        return render_template('profile.html', account=account, cards=user.get_cards())
    # User is not logged in redirect to login page
    return redirect(url_for('login'))


@app.route('/keywallet/card/<int:card_id>')
def card(card_id):
    # dh = DatabaseHandler(mysql)
    dh = Factory.create_database_handler(mysql)
    # Fetch the card details from the database based on its ID
    card = dh.get_card_by_id(card_id)
    # Render the card page template with the card details
    return render_template('card.html', card=card)


@app.route('/keywallet/scan')
def scan():
    return render_template('scan.html')


@app.route('/process_qr_code', methods=['POST'])
def process_qr_code():
    # Get the JSON data from the request
    data = request.json
    qr_data = data['qr_data']
    qr_data = qr_data.replace("'", '"')

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
        # cur = mysql.connection.cursor()
        # cur.execute(
        #     "INSERT INTO cards (`key`, company, imp_path, account_id) VALUES (%s, %s, %s, %s)",
        #     (card_key, card_company, img_path, user_id)
        # )
        # mysql.connection.commit()
        # cur.close()
        dh = Factory.create_database_handler(mysql)
        dh.add_new_card(card_key, card_company, img_path, user_id)
        return jsonify({'redirect_url': url_for('card_added')}), 200
        # return render_template('card_added.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/card_added')
def card_added():
    return render_template('card_added.html')


@app.route('/keywallet/change_password', methods=['GET', 'POST'])
def change_password():
    dh = Factory.create_database_handler(mysql)
    # Check if the user is logged in
    if not Factory.use_session_manager().is_logged_in():
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))

    msg = ''

    account = dh.get_account_data_by_id(session['id'])
    # print(account['email'])
    user = User()
    user.input_username(account['username'])
    user.input_password(account['password'])
    user.input_email(account['email'])

    if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
        # Create variables for easy access
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            user.input_password(new_password)
            msg = 'New password and confirm password do not match!'
        else:
            # Hash the old password for comparison
            old_password_hashed = hashlib.sha1((old_password + app.secret_key).encode()).hexdigest()
            print(old_password_hashed)
            # # Check if the old password is correct
            # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cur.execute('SELECT * FROM accounts WHERE id = %s AND password = %s', (session['id'], old_password_hashed))
            # account = cur.fetchone()
            account = dh.check_password(session['id'], old_password_hashed)

            if account:
                # Hash the new password
                new_password_hashed = Factory.use_password_manager().hash_password(new_password, app.secret_key)
                user.input_hashed_password(new_password_hashed)
                #
                # # Update the password in the database
                # cur.execute('UPDATE accounts SET password = %s WHERE id = %s', (new_password_hashed, session['id']))
                # mysql.connection.commit()
                dh.update_password(user.get_hashed_password(), session['id'])
                msg = 'Password successfully changed!'
            else:
                msg = 'Incorrect old password!'

    # Fetch account and card details again to render the profile page
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    # account = cur.fetchone()
    account = dh.get_account_data_by_id(session['id'])
    # cur.execute('SELECT * FROM cards WHERE account_id = %s', (session['id'],))
    # cards = cur.fetchall()
    cards = dh.get_card_by_account_id(session['id'])
    user.update_cards(cards)

    return render_template('profile.html', account=account, cards=user.get_cards(), msg=msg)

@app.route('/keywallet/qr_generator')
def qr_generator():
    return render_template('qr_generator.html')

@app.route('/keywallet/generate_qr', methods=['POST'])
def generate_qr():
    company = request.form["company"]
    key = request.form["key"]

    card_data = {
        "key": key,
        "company": company,
    }
    print(card_data)


    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=5)
    qr.add_data(card_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    byteIO = BytesIO()
    img.save(byteIO, 'PNG')
    byteIO.seek(0)
    return send_file(byteIO, mimetype='image/png')
