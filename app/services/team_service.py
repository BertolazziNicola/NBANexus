# Base modules
import time
import re
import os
import requests

# Other modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bson import ObjectId

# MongoDB
from app.configs.db import mongo

def import_teams_with_selenium(save_images, overwrite):
    """
    This function scrapes NBA team information from the official NBA website (https://www.nba.com/teams).
    It uses Selenium in headless mode to load the page, extract team data, and save it into a MongoDB database.
    
    The function collects the following information for each team:
        - Team ID (unique identifier)
        - Team Name (full name of the team)
        - Team Slug (short identifier for the team)
        - Team Image (optional - logo in SVG format)
        - Division Name (the conference/region the team belongs to)
    
    Images can optionally be downloaded based on the value of `save_images`. 
    If `overwrite` is set to True, any existing team data in the database with the same team ID will be replaced.

    Parameters:
        save_images (bool): If True, the function will download and save the team logos (SVG images).
        overwrite (bool): If True, the function will overwrite any existing team data in the database.

    Returns:
        bool: Returns True if the scraping and insertion into the database were successful, False otherwise.
    """
    
    # Setup driver headless for https://www.nba.com/teams
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs the browser in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration (useful in some environments)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.nba.com/teams")

    time.sleep(4)

    # Find all the team divisions (zones) on the page
    divisions = driver.find_elements(By.CLASS_NAME, "TeamDivisions_division__u3KUS")

    for division in divisions:
        # Extract the name of the zone (e.g., "Eastern Conference", "Western Conference")
        division_name = division.find_element(By.CLASS_NAME, "TeamDivisions_divisionName__KFlSk").text

        # Find all the teams in this zone
        teams = division.find_elements(By.CLASS_NAME, "TeamFigure_tf__jA5HW")

        for team in teams:
            # Initialize a dictionary to hold the team's data
            team_json = {
                "division": division_name
            }

            # Try to extract the team ID from the team's link (REQUIRED)
            try:
                temp_id = team.find_element(By.CLASS_NAME, "TeamFigureLink_teamFigureLink__uqnNO").get_attribute("href")

                # Extract the team ID from the URL using a regular expression
                team_json["team_id"] = re.search(r"/team/(\d+)", temp_id).group(1)
            except Exception as e:
                return False

            # Try to extract the team's name and slug (REQUIRED)
            try:
                temp_team_name = team.find_element(By.CLASS_NAME, "TeamFigure_tfMainLink__OPLFu")

                # Extract the slug from the team URL (e.g., 'celtics')
                team_json["slug"] = re.search(r"nba\.com/(\w+)", temp_team_name.get_attribute("href")).group(1)

                # Store the team name (e.g., 'Boston Celtics')
                team_json["name"] = temp_team_name.text
            except Exception as e:
                return False

            # Try to extract the team's image URL (OPTIONAL)
            try:
                # Find the <figure> tag containing the team's image and extract the image source URL
                img_src = f"https://cdn.nba.com/logos/nba/{team_json['team_id']}/global/L/logo.svg"
                
                team_json["img_src"] = img_src

                # Define the path where images will be saved
                path = os.getenv('TEAMS_LOGO_PATH')

                # If save_images is True, download and save the image
                if save_images and img_src:
                    # Create the directory to store images if it doesn't exist
                    os.makedirs(path, exist_ok=True)

                    # Download the image and save it
                    image_name = os.path.join(path, f"{team_json['slug']}.svg")

                    if not os.path.exists(image_name) or overwrite:
                        img_data = requests.get(img_src).content

                        with open(image_name, 'wb') as handler:
                            handler.write(img_data)
            except Exception as e:
                team_json["img_src"] = None

            try:
                # Save data into DB
                if overwrite:
                    mongo.db['teams'].delete_one({
                        'team_id': team_json["team_id"]
                    })
                        
                existing_team = mongo.db['teams'].find_one({
                        'team_id': team_json["team_id"]
                })

                if existing_team is None:
                    # Insert the new team data
                    mongo.db['teams'].insert_one(team_json)
            except Exception:
                return False

    # Close the browser once the scraping is complete
    driver.quit() 
    return True

def get_teams():
    try:
        result = mongo.db['teams'].find()

        # Convert ObjectId to string
        result_list = []
        for item in result:
            item['_id'] = str(item['_id'])  # Convert the ObjectId to string
            result_list.append(item)

        return result_list
    except Exception as e:
        # Handle any errors by returning None
        return None