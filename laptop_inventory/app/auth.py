from flask import Blueprint, request, session, jsonify
from app import mysql, bcrypt, mongo_client
import re  # Regular expressions for email validation

auth_bp = Blueprint('auth', __name__)

def validate_registration_data(data):
    """Validate registration data."""
    errors = []

    # Validate username
    username = data.get('username')
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters long.")

    # Validate password
    password = data.get('password')
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters long.")
    elif not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one letter and one number.")

    # Validate email
    email = data.get('email')
    if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        errors.append("Invalid email address.")

    # Validate role
    role = data.get('role', 'user')  # Default role is 'user'
    if role not in ['admin', 'user']:
        errors.append("Role must be either 'admin' or 'user'.")

    return errors


def validate_login_data(data):
    """Validate login data."""
    errors = []

    # Validate username
    if not data.get('username'):
        errors.append("Username is required.")

    # Validate password
    if not data.get('password'):
        errors.append("Password is required.")

    return errors


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate registration data
    validation_errors = validate_registration_data(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400

    username = data['username']
    password = data['password']
    email = data['email']
    role = data.get('role', 'user')  # Default role is user

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert into MySQL
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, role) VALUES (%s, %s, %s, %s)",
            (username, hashed_password, email, role),
        )
        mysql.connection.commit()
    except Exception as e:
        return jsonify({"error": "User already exists or invalid data."}), 400
    finally:
        cursor.close()

    # Insert into MongoDB
    mongo_client.laptop_inventory.users.insert_one({
        "username": username,
        "password_hash": hashed_password,
        "email": email,
        "role": role
    })

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate login data
    validation_errors = validate_login_data(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400

    username = data['username']
    password = data['password']

    # Fetch user from MySQL
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid username or password."}), 401

    session['user_id'] = user['id']
    session['username'] = user['username']
    session['role'] = user['role']  # Store role for access control

    return jsonify({"message": f"Logged in as {user['role']} successfully"}), 200

# User Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.clear()  # Clear all session data
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "No active session found"}), 400