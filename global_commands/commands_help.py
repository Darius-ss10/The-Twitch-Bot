# Imports
import sys
sys.path.append("..")
from time import time
import global_variables as gv


# Commands (help)
def commands(self, user, other_user):
    c = self.connection

    link = "https://prnt.sc/bj9u8mLUnMXO"

    # Basic command
    if other_user is None or other_user[0] != '@':
        message = f"{user}, here you have all bot's commands: {link}"

    # Command + tag to another user
    else:
        message = f"{other_user}, here you have all bot's commands: {link}"

    c.privmsg(self.channel, message)


# Help Vons
def help(self, user, other_user):
    c = self.connection

    link_vons = "https://prnt.sc/j4e8PkoqgjXG"
    link_commands = "https://prnt.sc/bj9u8mLUnMXO"

    if user is not None:
        # Basic command
        if other_user is None or other_user[0] != '@':
            message = f"{user}, here you have informations about Vons: {link_vons}"

        # Command + tag to another user
        else:
            message = f"{other_user}, here you have informations about Vons: {link_vons}"

    # Cooldown for the automatic command
    else:
        message = f"{other_user}, here you have informations about Vons: {link_vons}"
        message2 = f"{other_user}, here you have all bot's commands: {link_commands}"
        c.privmsg(self.channel, message2)

        gv.time_help = time() + 1800

    c.privmsg(self.channel, message)



# Message for the first time chatters
def new_user(self, user):
    c = self.connection

    message = f"{user}, welcome to our chat!"
    c.privmsg(self.channel, message)
