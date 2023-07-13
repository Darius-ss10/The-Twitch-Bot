# Imports
import requests
import global_variables as gv
from get_access_token import get_access_token

def get_user_id(username):

    if username[0] == '@':
        username = username[1:]

    url = 'https://api.twitch.tv/helix/users'
    params = {'login': username}

    headers = {
        'Authorization': f"Bearer {gv.bot_access_token}",
        'Client-ID': gv.bot_client_id
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200 and len(response.json()["data"]) > 0:
        # Request successful
        response_json = response.json()
        # Process the response JSON as needed
        return response_json["data"][0]["id"]
    elif response.status_code == 200 and len(response.json()["data"]) == 0:
        # Request successful, but user not found
        print(f"User {username} not found")
    else:
        # Request failed
        print(f"API request failed with status code {response.status_code}: {response.text}")
        gv.bot_access_token = get_access_token()
        return get_user_id(username)