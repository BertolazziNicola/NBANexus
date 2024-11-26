import requests
import json
import os  # Per gestire le operazioni sui file e sulle cartelle
from datetime import datetime

# URL dell'API
url = "https://stats.nba.com/stats/playerindex?College=&Country=&DraftPick=&DraftRound=&DraftYear=&Height=&Historical=1&LeagueID=00&Season=2024-25&TeamID=0&Weight="

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Effettuare la richiesta GET
response = requests.get(url, headers=headers)

# Controllare lo stato della risposta
if response.status_code == 200:
    data = response.json()  # Convertire in formato JSON
    print("Dati ottenuti con successo!")
    
    # Creare la cartella se non esiste
    os.makedirs('./data', exist_ok=True)

    # Creare un nome di file con la data attuale
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Formato data e ora
    file_name = f'./scripts/extra/data/version-{current_datetime}.json'

    # Salvare i dati in un file JSON
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)  # Scrivere i dati in formato JSON
    print(f"Dati salvati in {file_name}")
else:
    print(f"Errore nella richiesta: {response.status_code}")
