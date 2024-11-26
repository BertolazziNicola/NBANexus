# Base modules
from functools import wraps

# Other modules
import bcrypt
from flask import session, redirect, url_for

# MongoDB
from app.configs.db import mongo

def login_required():
    """Decorator to check if the user is logged in."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('admin.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_user(user, remember=False):
    """Login a user and store their user in the session."""
    session['user'] = {
        '_id': str(user['_id']),
        'email': user['email'],
        'api_key': user['api_key'],
        'role': user['role'],
    }
    if remember:
        session.permanent = True

def logout_user():
    """Logout the user by removing them from the session."""
    session.pop('user', None)

def hash_password(password):
    """Hash a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.
    
    Returns:
        bytes: The hashed password.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Convert the hashed password from bytes to string
    return hashed_password_bytes.decode('utf-8')

def check_password(password, hashed_password):
    """Verify if a plaintext password matches the hashed password.

    Args:
        password (str): The plaintext password to check.
        hashed_password (str): The hashed password for comparison.
    
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def is_valid_api_key(api_key):
    """
    Checks if the provided API key exists in the database.

    This function searches for the given API key in the 'users' collection of the database.
    If the API key is found, it returns True; otherwise, it returns False.

    Parameters:
        api_key (str): The API key to check in the database.

    Returns:
        bool: True if the API key exists, False if it does not or if an error occurs.
    """
    try:
        # Query the database to check if the API key exists
        user_api_key = mongo.db['users'].find_one(
            { 'api_key': api_key },  # Search for the provided API key
            { 'api_key': 1 }         # Only return the 'api_key' field
        )

        # Return True if the API key is found, otherwise return False
        if user_api_key:
            return True
        return False
    except Exception as e:
        return False