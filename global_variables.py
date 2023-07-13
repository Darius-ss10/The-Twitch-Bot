# Global variables
def initialize():
    # Variables for the owner of the channel and the bot
    # Indicates the streamer's username
    global owner
    owner = ""  # Here you have to put the channel the bot will connect to
    owner = owner.lower()

    # Indicates the streamer's ID
    global owner_id
    owner_id = None  # Here the streamer's ID will be put automatically

    # Indicates the bot's username
    global bot_username
    bot_username = ""  # Here you have to put the bot's username
    bot_username = bot_username.lower()

    # Indicates the bot's ID
    global bot_id
    bot_id = None  # Here the bot's ID will be put automatically

    # Indicates the bot's OATH token
    global bot_OATH_token
    bot_OATH_token = ""  # Here you have to put the OATH token of the bot

    # Indicates the bot's user access token
    global bot_access_token
    bot_access_token = None  # Here the user access token of the bot will be put automatically

    # Indicates the bot's client ID
    global bot_client_id
    bot_client_id = ""  # Here you have to put the client ID of the bot

    # Indicates the bot's client secret
    global bot_client_secret
    bot_client_secret = ""  # Here you have to put the client secret of the bot