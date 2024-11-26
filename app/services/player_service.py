# Base modules

# Other modules
from flask import jsonify

# MongoDB
from app.configs.db import mongo

# Services
from app.services.db_service import check_and_create_collection, check_collection
from app.services.request_service import get_nba_players_request

def add_player_to_collection(collection_name, player_data):
    """Add a new player to the specified collection.
    
    Args:
        collection_name (str): The name of the collection to which the player will be added.
        player_data (dict): A dictionary containing player details to be added.
        
    Returns:
        None
    """
    mongo.db[collection_name].insert_one(player_data)
    
def import_players_into_collection(season, overwrite, collection):
    """Import all the players from a specific NBA season into the MongoDB collection.

    Args:
        season (str): The season in the format 'YYYY-YY'.
        overwrite (bool): Indicates whether to overwrite the existing player if it exists.
        collection (str): The collection name.

    Returns:
        bool: True if the import was successful, False otherwise.
    """
    
    # Retrieve player data from the NBA API for the specified season
    data = get_nba_players_request(season)

    # Extract the season from the API response (assuming it's part of the response headers or data)
    api_season = data['parameters']['Season']
    
    # Check if the collection exists; if not, create it
    check_and_create_collection(collection)
    if not check_collection(collection):
        return False
        
    try:
        # Extract headers and row data from the retrieved data
        headers = data['resultSets'][0]['headers']
        rowSet = data['resultSets'][0]['rowSet']

        # Iterate through each row of player data
        for row in rowSet:
            # Create a dictionary for player data, using headers as keys in lowercase
            player_data = {headers[i].lower(): row[i] for i in range(len(headers))}

            # Check if the player data is an All-Time or season
            if player_data.get('roster_status') == 1:
                season_type = season
            else:
                season_type = 'alltime'

            player_data['season'] = season_type

            if overwrite:
                mongo.db[collection].delete_one({
                    'person_id': player_data.get('person_id'),
                    'season' : season_type
                })
                    
            existing_player = mongo.db[collection].find_one({
                    'person_id': player_data.get('person_id'),
                    'season': season_type
            })

            if existing_player is None:
                # Insert the new player data
                mongo.db[collection].insert_one(player_data)


        # Return True if all data was imported successfully
        return True
    except Exception as e:
        # Handle any exceptions that occur during the import process
        return False  # Return False if an error occurred

def get_players_imported_dates():
    """
    Retrieves all the unique seasons from the 'players' collection in MongoDB, 
    excluding "alltime", and returns the results sorted by season in ascending order.

    This function performs an aggregation pipeline on the MongoDB collection 'players', 
    where it:
        1. Filters out documents with the season "alltime".
        2. Groups the results by the 'season' field.
        3. Sorts the seasons in ascending order.

    Returns:
        JSON response: A list of unique seasons (excluding "alltime") sorted in ascending order.
        If an error occurs, returns None.
    """
    try:
        # Perform the aggregation query to get all unique seasons, excluding "alltime"
        result = mongo.db['players'].aggregate([
            { "$match": { "season": { "$ne": "alltime" } } },

            { "$group": {
                "_id": "$season",
                "count": { "$sum": 1 } # Count players for season
            } },

            { "$sort": { "_id": -1 } }
        ])

        # Return the result as a list of JSON objects
        return list(result)
    except Exception as e:
        # Handle any errors by returning None
        return None