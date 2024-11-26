# Base modules
import uuid

# Other modules
from bson import ObjectId

# MongoDB
from app.configs.db import mongo

# Services
from app.services.auth_service import hash_password, is_valid_api_key

def check_admin_user_id(id):
    """Check if the admin user exists by _id.
    
    Args:
        id (str): The id of the user.
        
    Returns:
        bool: True if the user exists, False otherwise.
    """
    user = mongo.db['users'].find_one({"_id": id, "role": "admin"})
    return user is not None

def check_admin_user_email(email):
    """Check if the admin user exists by email.
    
    Args:
        email (str): The email of the user.
        
    Returns:
        bool: True if the user exists, False otherwise.
    """
    user = mongo.db['users'].find_one({"email": email, "role": "admin"})
    return user is not None

def create_admin_user(email, password):
    """
    Creates a new admin user in the database if the email is not already in use.

    This function:
    - Checks if the email is already associated with an existing admin user.
    - Generates a unique API key and hashes the password.
    - Inserts the new user into the database with the role 'admin' and sets the user as active.

    Parameters:
        email (str): The new admin user's email address.
        password (str): The new admin user's plain-text password.

    Returns:
        bool: `True` if the user is successfully created, `False` if the user already exists or an error occurs.
    """
    # Check that the user doesn't exists
    if(not check_admin_user_email(email)):
        # Generate API key and check that doesn't exists
        api_key = str(uuid.uuid4())
        if(not is_valid_api_key(api_key)):
            try:
                # Hash password
                password = hash_password(password)
                
                # Create the user JSON 
                user = {
                    'email': email,
                    'password': password,
                    'api_key': api_key,
                    'role': 'admin',
                    'is_active': True,
                }

                mongo.db['users'].insert_one(user)
                return True
            except Exception as e:
                return False

    return False

def change_admin_user_password(_id, new_password):
    """
    Change the password of an admin user in the database.

    This function takes the user ID and a new password, hashes the new password,
    attempts to update the password in the database for the specified user ID,
    and returns True if the operation is successful (i.e., the password is updated),
    or False if an error occurs or if no matching user is found.

    Parameters:
        _id (ObjectId): The user ID (as a ObjectId) whose password needs to be changed.
        new_password (str): The new password to be set for the user.

    Returns:
        bool: True if the password was successfully changed, False if an error occurred
              or if no user matched the provided ID.
    """
    try:
        # Hash the new password before updating
        hashed_password = hash_password(new_password)

        # Update the password in the database
        result = mongo.db['users'].update_one(
            { '_id': _id },
            { '$set': { 'password': hashed_password } }
        )

        # Check if the update was successful (matched at least one document)
        if result.matched_count > 0:
            return True
        else:
            return False

    except Exception as e:
        return False
    
def get_users_by_roles(roles):
    """
    Retrieve users based on their roles from the database.

    This function takes a list of roles and queries the 'users' collection to find users 
    whose 'role' field matches one of the roles in the list. If no roles are provided or if 
    the roles list is empty, the function retrieves all users from the collection.

    Parameters:
        roles (list): A list of roles to filter users by. If the list is empty or None,
                    all users will be retrieved.

    Returns:
        list: A list of users that match the role criteria, excluding the 'password', 'api_key' fields. 
            If an error occurs during the query, None will be returned.
    """
    try:
        # Check if roles are provided and are not empty
        if roles is None or len(roles) == 0:
            result = mongo.db['users'].find(
                {},  # Empty filter (all users)
                {'password': 0, 'api_key': 0}  # Exclude 'password', 'api_key'
            )
        else:
            result = mongo.db['users'].find(
                {'role': {'$in': roles}},  # Filter by role
                {'password': 0, 'api_key': 0}  # Exclude 'password', 'api_key'
            )

        # Convert the result cursor to a list and handle ObjectId serialization
        users_list = []
        for user in result:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            users_list.append(user)

        # Return the result
        return users_list

    except Exception as e:
        return None

def delete_user(_id):
    """
    Delete a user by their ID.
    
    Args:
        _id (ObjectId): The ID of the user to be deleted.
        
    Returns:
        bool: True if the user was deleted, False if an error occurred.
    """
    try:
        result = mongo.db['users'].delete_one({'_id': ObjectId(_id)})
        return result.deleted_count > 0
    except Exception as e:
        return False