# Imports
import requests
import global_variables as gv
import sqlite3
import os
from dotenv import load_dotenv

# Locate the database
DATABASE = os.path.abspath("base.db")

def get_refresh_token():

    token_url = 'https://id.twitch.tv/oauth2/token'

    data = {
        'client_id': gv.bot_client_id,
        'client_secret': gv.bot_client_secret,
        'code': gv.bot_authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:3000'
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        # Request successful
        response_json = response.json()

        # Access the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM Tokens")
        result = cursor.fetchone()

        if result[0] == 0:
            # Table is empty, perform an insert
            cursor.execute("INSERT INTO Tokens (refresh_token) VALUES (?)", (response_json["refresh_token"],))
        else:
            # Table is not empty, replace the first value
            cursor.execute("UPDATE Tokens SET refresh_token = ? WHERE rowid = 1", (response_json["refresh_token"],))
        # Save and close the database
        conn.commit()
        conn.close()

        print("Refresh token request successful.")

    else:
        # Request failed
        raise Exception(f"Refresh token request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    load_dotenv()
    gv.initialize()
    get_refresh_token()
