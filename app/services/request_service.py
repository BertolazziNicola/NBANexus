# Base modules
import requests

def get_nba_players_request(season):
    """Fetch NBA player data for the specified season from the NBA stats API.
    
    Args:
        season (str): The NBA season in the format 'YYYY-YY', e.g., '2024-25', '2012-13', '2019-20', '1999-00'.
        
    Returns:
        dict or None: A dictionary containing player data if the request is successful (HTTP 200),
                      or None if the request fails.
    """
    # API URL with dynamic season parameter
    url = f'https://stats.nba.com/stats/playerindex?College=&Country=&DraftPick=&DraftRound=&DraftYear=&Height=&Historical=1&LeagueID=00&Season={season}&TeamID=0&Weight='

    # Define the headers for the HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # Make a GET request to the API URL
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the data (valid request)
        data = response.json()
        return data
    else:
        # Return None (invalid request)
        return None
