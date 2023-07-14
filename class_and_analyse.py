# Imports
import irc.bot
from time import time
import global_variables as gv
from points import points_chat, points_user, mods_points

# The TwitchBot class
class TwitchBot(irc.bot.SingleServerIRCBot):

    # The bot connects to Twitch
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = f"#{channel}"

        # Alternative to the section above
        self.channel_id = gv.owner_id  # Here you have to hardcode the channel id of the channel the bot will connect to

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print(f"Connecting to {server} on port {port} ...")
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, f"oauth:{token}")], username, username)


    # The bot connects to the channel's chat
    def on_welcome(self, c, e):
        print(f"Joining {self.channel}")

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print(f"Joined {self.channel}")
        c.privmsg(self.channel, "HeyGuys")


    # The bot analyses chat messages
    def on_pubmsg(self, c, e):

        # Add chatter
        if e.tags["display-name"] not in gv.chat and e.tags["display-name"] not in gv.no_vons:
            gv.chat.append(e.tags["display-name"])

        if e.tags["display-name"] not in gv.all and e.tags["display-name"] not in gv.no_vons:
            gv.all.append(e.tags["display-name"])

        # Vons for chatters
        if time() > gv.time_points:
            points_chat()

        # Verify if the chatter is a sub
        if e.tags["subscriber"] == "1" and e.tags["display-name"] not in gv.all_subs \
                and e.tags["display-name"] not in gv.no_vons:

            user = e.tags["display-name"]
            if user in gv.all_plebs:
                gv.all_plebs.remove(user)
            gv.all_subs.append(user)


        # Verify if the chatter isn't a sub
        elif e.tags["subscriber"] == "0" and e.tags["display-name"] not in gv.all_plebs \
                and e.tags["display-name"] not in gv.no_vons:

            user = e.tags["display-name"]
            if user in gv.all_subs:
                gv.all_subs.remove(user)
            gv.all_plebs.append(user)

        # Global commands
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]

            # Verify how many Vons have the user
            if cmd == "vons":
                user = e.tags["display-name"]
                try:
                    other_user = e.arguments[0].split()
                    other_user = other_user[1]
                except:
                    other_user = None
                points_user(self, user, other_user)


        # MODS only commands
        if e.arguments[0][:1] == '!' and (e.tags["mod"] == "1" or e.tags["display-name"].lower() == gv.owner):
            cmd = e.arguments[0].split(' ')[0][1:]
            mod = e.tags["display-name"]

            # Mods can give Vons to chatters
            if cmd == "give_vons":
                try:
                    info = e.arguments[0].split()
                    user = info[1]
                    nr_points = int(info[2])
                except:
                    user = None
                    nr_points = None
                mods_points(self, mod, user, nr_points, True)
