import requests
import sqlite3
import os
import global_variables as gv

# Locate the database
DATABASE = os.path.abspath("base.db")

def get_access_token():

    token_url = 'https://id.twitch.tv/oauth2/token'

    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT refresh_token FROM Tokens ORDER BY rowid LIMIT 1")
    result = cursor.fetchone()

    if result:
        first_value = result[0]
    else:
        print("Table is empty")

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': first_value,
        'client_id': gv.bot_client_id,
        'client_secret': gv.bot_client_secret
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        # Request successful
        response_json = response.json()

        # Update the refresh token
        cursor.execute("UPDATE Tokens SET refresh_token = ? WHERE rowid = 1", (response_json["refresh_token"],))
        # Save and close the database
        conn.commit()
        conn.close()
        return response_json['access_token']
        # Use the new access_token for further API requests or store it securely
    else:
        # Request failed
        raise Exception(f"Access token request failed with status code {response.status_code}: {response.text}")
