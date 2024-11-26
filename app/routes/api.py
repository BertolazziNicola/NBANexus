# Base modules

# Other modules
from flask import url_for, request, Blueprint, jsonify

# Services
from app.services.player_service import import_players_into_collection, get_players_imported_dates
from app.services.auth_service import is_valid_api_key
from app.services.admin_service import get_users_by_roles
from app.services.team_service import import_teams_with_selenium, get_teams

# Validators
from app.validators.api_validator import validate_import_players, validate_import_teams

# Blueprint
api = Blueprint('api', __name__)

@api.route("/", methods=["GET"])
def get_players():
    """
    Handles the return of all the players of a season into the collection 'players'.

    This function receives a GET request containing JSON data with....
    Otherwise a failed message will appear.

    Returns:
        A JSON response,
        with appropriate HTTP status codes:
            - 200 if all has been returned successfully.
            - 400 if the input data is invalid or a issue with the players returning.
    """
    data = request.json

    # TODO
    
    
@api.route("/import/players", methods=["POST"])
def post_import_players():
    """
    Handles the creation of all the players of a season into the collection 'players'.

    This function receives a POST request containing JSON data with
    the required field 'season'. It validates the incoming data, checks
    if a collection with the given name can be created and add the players.
    If the players are successfully created, it returns
    a success message along with the name of the created collection.
    Otherwise a failed message will appear.

    Returns:
        A JSON response indicating the result of the operation,
        with appropriate HTTP status codes:
            - 200 if all has been created successfully.
            - 400 if the input data is invalid or a issue with the players creation.
            - 403 if the api key is invalid.
    """
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return {"message": "Invalid POST request, api-key not set"}, 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return {"message": "Invalid POST request, api-key not found in the database"}, 403

    data = request.json

    # Validate the data
    validated_data, errors = validate_import_players(data)
    if errors:
        return {"message": "Invalid POST request, season must be YYYY-YY format"}, 400

    # Set season and collection_name variables
    season = validated_data["season"]
    collection_name = "players"
    overwrite = validated_data["overwrite"]

    # Set response data
    response = {
        "collection_name": collection_name,
        "season": season,
    }

    # Attempt to import players into the collection
    if import_players_into_collection(season, overwrite, collection_name):    
        response["message"] = "Players imported successfully"
        return response, 200

    # If players were not imported
    response["message"] = "Players not imported"
    return response, 400

@api.route("/import/players", methods=["GET"])
def get_import_dates():
    """
    Handles fetching the dates of all imported records.

    This function processes a GET request to retrieve the dates
    of all previously imported records. It validates the incoming
    API key from the request headers and ensures it is valid and
    authorized. If the API key is valid, the function queries the
    database or backend service to fetch the list of imported dates
    and returns them in the response.

    Returns:
        A JSON response with the following structure:
            - "message": A string indicating the operation's result.
            - "dates": A list of dates representing previously imported records.
        HTTP Status Codes:
            - 200: If the operation succeeds and dates are retrieved.
            - 403: If the API key is missing or invalid.
    """
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "Invalid GET request"}), 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return jsonify({"message": "Invalid GET request, api-key not found in the database"}), 403
    
    # Set response data and send it
    response = {
        "message" : "All imports dates returned",
        "dates" : get_players_imported_dates()
    }

    return jsonify(response), 200

@api.route("/import/teams", methods=["POST"])
def post_import_teams():
    """
    API Endpoint to import basketball teams into the database.

    This function processes a POST request to import basketball teams by:
    1. Validating the API key provided in the request header.
    2. Validating the data received in the JSON body (specifically, 
       ensuring that 'save-images' and 'overwrite' are boolean).
    3. Attempting to import teams via a selenium-based web scraping process 
       that fetches information from the NBA website.
    4. Optionally downloading images for the teams based on the 'save-images' flag.

    If the teams are successfully imported, it returns a response with the 
    status message "Teams imported successfully". If there are issues with the
    API key, validation, or team import, it returns an error message.

    Parameters:
        - `save-images` (bool): Flag indicating if team images should be downloaded and saved.
        - `overwrite` (bool): Flag indicating if existing teams should be overwritten in the database.

    Returns:
        - Response (JSON): A JSON response containing a message indicating the outcome of the import.
            - If successful: {"message": "Teams imported successfully", "save-images": <bool>, "overwrite": <bool>}
            - If failed: {"message": "Teams not imported", "save-images": <bool>, "overwrite": <bool>}
    """
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return {"message": "Invalid POST request, api-key not set"}, 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return {"message": "Invalid POST request, api-key not found in the database"}, 403

    data = request.json

    # Validate the data
    validated_data, errors = validate_import_teams(data)
    if errors:
        return {"message": "Invalid POST request, save-images and overwrite must be boolean"}, 400

    save_images = validated_data['save-images']
    overwrite = validated_data['overwrite']

    # Set response data
    response = {
        "save-images": save_images,
        "overwrite" : overwrite
    }

    # Attempt to import teams
    if import_teams_with_selenium(save_images, overwrite):    
        response["message"] = "Teams imported successfully"
        return response, 200

    # If teams were not imported
    response["message"] = "Teams not imported"
    return response, 400

@api.route("/users", methods=["GET"])
def get_users():
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "Invalid GET request"}), 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return jsonify({"message": "Invalid GET request, api-key not found in the database"}), 403
    
    # Set response data and send it
    response = {
        "message" : "All users returned",
        "users" : get_users_by_roles(None)
    }

    return jsonify(response), 200

@api.route("/import/teams", methods=["GET"])
def get_import_teams():
    # Validate api-key
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return jsonify({"message": "Invalid GET request"}), 403

    # Check if api key is not valid
    if not is_valid_api_key(api_key):
        return jsonify({"message": "Invalid GET request, api-key not found in the database"}), 403
    
    
    # Set response data and send it
    response = {
        "message" : "All imports teams returned",
        "teams" : get_teams()
    }

    return jsonify(response), 200