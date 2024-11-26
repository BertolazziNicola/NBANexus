# Base modules

# Other modules
from flask import url_for, request, render_template, Blueprint, redirect, flash, session, jsonify
from bson import ObjectId

# MongoDB
from app.configs.db import mongo

# Services
from app.services.admin_service import create_admin_user, change_admin_user_password, delete_user
from app.services.auth_service import check_password, login_required, login_user, logout_user, is_valid_api_key

# Validators
from app.validators.admin_validator import validate_login, validate_profile, validate_create_user, validate_modify_user

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required()
def index():
    return render_template('auth/login.html')

@admin.route('/login')
def login():
    # create_admin_user('admin@gmail.com', 'Admin$00')
    return render_template('auth/login.html')

@admin.route('/login', methods=['POST'])
def login_post():
    """
    Handles the POST request for user login in the admin panel.

    This function performs the following steps:
    1. Validates the login form data.
    2. Checks if the provided email exists and matches an 'admin' role.
    3. Verifies the provided password against the stored password hash.
    4. If all checks pass, logs the user in and redirects to the index page.
    5. If any validation or authentication fails, an appropriate error message is displayed
       and the user is redirected back to the login page.

    Flash messages are used to inform the user of any issues:
    - "Invalid data" if the input data fails validation.
    - "Inexistent user" if the email is not associated with an admin user.
    - "Wrong password" if the entered password does not match the stored hash.
    
    Arguments:
        None

    Returns:
        Redirects to the appropriate URL based on the outcome of the login attempt:
        - Redirects to the login page with an error message if any validation fails.
        - Redirects to the index page if the login is successful.
    """
    # Get data
    data = request.form.to_dict()

    # Validate the data
    validated_data, errors = validate_login(data)
    if errors:
        flash("Invalid data", "danger")
        return redirect(url_for('admin.login'))
    
    # Get user from DB and check that exists
    user = mongo.db['users'].find_one({ 'email': validated_data['email'], 'role':'admin' })
    if user is None:
        flash("Inexistent user", "danger")
        return redirect(url_for('admin.login'))

    # Wrong password
    if not check_password(validated_data['password'], user['password']):
        flash("Wrong password", "danger")
        return redirect(url_for('admin.login'))
    
    # User logged in
    login_user(user, remember=validated_data['remember'])

    return redirect(url_for('base.index'))

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin.route('/profile')
@login_required()
def profile():
    return render_template('pages/admin/profile.html')

@admin.route('/profile', methods=['POST'])
@login_required()
def profile_post():
    """
    Handles the POST request for updating user profile information, including changing the password.
    
    This function performs the following steps:
    1. Retrieves and validates the form data submitted by the user.
    2. Verifies the provided password by comparing it to the stored password in the database.
    3. If the password is correct, attempts to update the user's password in the database.
    4. If successful, flashes a success message and redirects to the profile page.
    5. If the update fails (due to an error or exception), flashes an error message and redirects back to the profile page.

    Flash messages:
    - "Invalid data": if the provided data is invalid.
    - "Wrong password": if the password verification fails.
    - "Data changed correctly": if the password is successfully updated.
    - "Data not changed. Please try again.": if there was an error during the password update process.

    Returns:
        Redirect to the profile page with a flash message indicating success or failure.
    """
    # Get data
    data = request.form.to_dict()

    # Validate the data
    validated_data, errors = validate_profile(data)
    if errors:
        flash("Invalid data", "danger")
        return redirect(url_for('admin.profile'))
    
    try:
        # Get user and check password 
        user = mongo.db['users'].find_one({ '_id': ObjectId(session['user']['_id']) })
        if not check_password(validated_data['password'], user['password']):
            flash("Wrong password", "danger")
            return redirect(url_for('admin.profile'))
        
        # Try to change password
        if change_admin_user_password(ObjectId(session['user']['_id']), validated_data['new-password']):
            flash("Data changed correctly", "success")
            return redirect(url_for('admin.profile'))
        
        flash("Data not changed. Please try again.", "danger")
        return redirect(url_for('admin.profile'))
    except Exception as e:
        flash("Data not changed. Please try again.", "danger")
        return redirect(url_for('admin.profile'))


@admin.route('/user/create', methods=['GET'])
@login_required()
def get_user_create():
    return render_template('pages/admin/user/create.html')

@admin.route('/user', methods=['GET'])
@login_required()
def get_user_modify():
    """
    Route to fetch user details for modification.
    
    This route checks if an '_id' query parameter is provided.
    If so, it attempts to fetch the corresponding user from the database.
    If the user exists, it renders a form populated with the user's data for modification.
    If no valid user is found or if '_id' is not provided, the user is redirected back 
    to the user list page.
    """
    # Check if _id is provided as a query parameter
    user_id = request.args.get('_id')
    
    if user_id:
        try:
            user = mongo.db['users'].find_one({'_id': ObjectId(user_id)})
                        
            # Check if user exists
            if user:
                # Return the template with the user data for editing
                return render_template('pages/admin/user/modify.html', user=user)
        except Exception as e:
            return redirect(url_for('admin.list_users'))

    return redirect(url_for('admin.list_users'))

@admin.route('/user/modify', methods=['POST'])
@login_required()
def post_user_modify():
    """
    Handles the modification of a user's data, including password change.

    Parameters:
        - data (dict): The form data containing the user ID, password, and new password.
    
    Flash Messages:
        - "Invalid data": If the input data doesn't pass validation.
        - "Wrong password": If the provided password doesn't match the current password.
        - "Data changed correctly": If the user data is successfully modified.
        - "User not changed": If there was an issue changing the user's data.
        - "Data not changed": If there was an unexpected error during the process.

    Redirects:
        - Redirects to the user modification page (with the user's `_id` in the URL) or the user list page, depending on the outcome.
    """
    # Get data
    data = request.form.to_dict()

    # Validate the data
    validated_data, errors = validate_modify_user(data)
    if errors:
        flash("Invalid data", "danger")
        return redirect(url_for('admin.list_users'))
    
    try:
        # Get user and check password 
        user = mongo.db['users'].find_one({ '_id': ObjectId(validated_data['_id']) })
        if not check_password(validated_data['password'], user['password']):
            flash("Wrong password", "danger")
            return redirect(url_for('admin.get_user_modify') + '?_id=' + validated_data['_id'])
        
        # Try to change password
        if change_admin_user_password(ObjectId(validated_data['_id']), validated_data['new-password']):
            flash("Data changed correctly", "success")
            return redirect(url_for('admin.get_user_modify') + '?_id=' + validated_data['_id'])
        
        flash("User not changed. Please try again.", "danger")
        return redirect(url_for('admin.get_user_modify') + '?_id=' + validated_data['_id'])
    except Exception as e:
        flash("Data not changed. Please try again.", "danger")
        return redirect(url_for('admin.list_users'))
    
@admin.route('/delete', methods=['POST'])
@login_required()
def post_delete_user():
    """
    Delete a user by their ID if authorized via API key.

    This function handles POST requests to delete a user from the database. 
    It validates the API key provided in the request headers, checks if the 
    API key is valid, and then attempts to delete the user identified by their ID.

    Args:
        None (data is retrieved from the request's JSON body and headers).

    Request JSON:
        {
            "_id": "string"  # The ID of the user to delete.
        }

    Request Headers:
        x-api-key: A valid API key for authorization.

    Returns:
        JSON Response:
            - 200: User successfully deleted.
                {"message": "User deleted"}
            - 403: Invalid or missing API key.
                {"message": "Invalid POST request"}
                {"message": "Invalid POST request, api-key not found in the database"}
            - 400: Deletion failed or invalid request.
                {"message": "Invalid POST request, user not deleted"}
    """
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "Invalid POST request"}), 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return jsonify({"message": "Invalid POST request, api-key not found in the database"}), 403

    try:
        # Get _id and try to delete user
        data = request.json

        if delete_user(data['_id']):
            # Set response data and send it
            return jsonify({
                "message" : "User deleted"
            }), 200

        return jsonify({"message": "Invalid POST request, user not deleted"}), 400
    except Exception as e:
        return jsonify({"message": "Invalid POST request, user not deleted"}), 400    

@admin.route('/user/create', methods=['POST'])
@login_required()
def post_user_create():
    """
    Create a new user.

    This route handles the creation of a new user. It accepts POST requests with user data,
    validates the data (email, password and role), checks if the email is already in use, and
    creates the user if everything is correct. If there are any validation errors or the email
    is already used, an error message is displayed. On successful creation, a success message
    is shown.

    If any exception occurs during the user creation process, the user will be redirected with
    a failure message.

    Flash Messages:
    - "Invalid data" if the input data is invalid.
    - "Email is already used" if the provided email is already in the database.
    - "User has been created" if the user is successfully created.
    - "User not created. Please try again." if the user creation fails.

    Redirects:
    - Always redirects to the 'admin.get_user_create' view, regardless of success or failure.

    Returns:
        Redirects to the user creation page with appropriate flash messages.
    """
    # Get data
    data = request.form.to_dict()

    # Validate the data
    validated_data, errors = validate_create_user(data)
    if errors:
        flash("Invalid data", "danger")
        return redirect(url_for('admin.get_user_create'))
    
    # Check is email is used
    user = mongo.db['users'].find_one({ 'email': validated_data['email'] })
    if user:
        flash("Email is already used", "danger")
        return redirect(url_for('admin.get_user_create'))
    
    if create_admin_user(validated_data['email'], validated_data['password']):
        flash("User has been created", "success")
        return redirect(url_for('admin.get_user_create'))
    
    flash("User not created. Please try again.", "danger")
    return redirect(url_for('admin.get_user_create'))

@admin.route('/users')
@login_required()
def list_users():
    return render_template('pages/admin/user/list.html')

@admin.route('/import/players')
@login_required()
def import_players():
    return render_template('pages/admin/player/import.html')

@admin.route('/import/teams')
@login_required()
def import_teams():
    return render_template('pages/admin/team/import.html')
