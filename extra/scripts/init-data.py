import requests

def send_request_for_season(url, season):
    # Corpo della richiesta
    body = {
        "season": season,
        "overwrite": True
    }
    headers = {
        'Authorization': 'Bearer your_token_here',
        'Content-Type': 'application/json'
    }
    try:
        # Invia la richiesta POST all'URL specificato con il body JSON
        response = requests.post(url, json=body, headers=headers)

        # Verifica se la richiesta ha avuto successo (status code 200)
        if response.status_code == 200:
            # Prova a ottenere i dati JSON dalla risposta
            data = response.json()
            # Print message and season (success)
            print("Season:", season, " --> ", data.get("message"))
        else:
            print(f"Errore nella risposta per la stagione {season}: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Gestisce eventuali eccezioni di rete
        print(f"Si è verificato un errore per la stagione {season}: {str(e)}")


url = 'http://localhost:5000/api/import'

# Elenco delle stagioni dal 2009-10 al 2023-24
# seasons = [
#     "2009-10", "2010-11", "2011-12", "2012-13", "2013-14",
#     "2014-15", "2015-16", "2016-17", "2017-18", "2018-19",
#     "2019-20", "2020-21", "2021-22", "2022-23", "2023-24"
# ]

# seasons = [
#     "2000-01", "2001-02", "2002-03", "2003-04", "2004-05",
#     "2005-06", "2006-07", "2007-08", "2008-09",
# ]

seasons = [
    "1980-81", "1981-82", "1982-83", "1983-84", "1984-85",
    "1985-86", "1986-87", "1987-88", "1988-89", "1989-90",
    "1990-91", "1991-92", "1992-93", "1993-94", "1994-95",
    "1995-96", "1996-97", "1997-98", "1998-99", "1999-00"
]

# Invia richieste per ogni stagione
for season in seasons:
    send_request_for_season(url, season)