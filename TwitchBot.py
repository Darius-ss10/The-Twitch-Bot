# Imports
from class_and_analyse import TwitchBot
import global_variables as gv
from get_access_token import get_access_token
from get_user_id import get_user_id
from dotenv import load_env


# The bot gets created
def main():

    gv.bot_access_token = get_access_token()
    gv.bot_id = get_user_id(gv.bot_username)
    gv.owner_id = get_user_id(gv.owner)

    bot = TwitchBot(gv.bot_username, gv.bot_client_id, gv.bot_OATH_token, gv.owner)
    bot.start()


# This starts the bot
if __name__ == "__main__":
    load_env()
    gv.initialize()
    main()
