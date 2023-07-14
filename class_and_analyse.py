# Imports
import irc.bot
from time import time
import global_variables as gv
from points import points_chat, points_user, mods_points
from games.games_roulette import roulette
from games.games_blackjack import blackjack, pen_blackjack
from games.games_activate import on, off, on_auto, off_auto

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
        # Information about the chatter
        tags = {}
        for i in range(len(e.tags)):
            tags[e.tags[i]["key"]] = e.tags[i]["value"]

        # Add chatter
        if tags["display-name"] not in gv.chat and tags["display-name"] not in gv.no_vons:
            gv.chat.append(tags["display-name"])

        if tags["display-name"] not in gv.all and tags["display-name"] not in gv.no_vons:
            gv.all.append(tags["display-name"])

        # Blackjack on/off auto
        # Off
        if gv.bj_off_auto and gv.on_bj and gv.user_blackjack is None:
            off_auto(self)

        if "The stream game has been updated to: Marbles On Stream" in e.arguments[0]:
            if gv.on_bj and gv.user_blackjack is None:
                off_auto(self)

            elif gv.on_bj and gv.user_blackjack is not None:
                gv.bj_off_automat = True

        elif "The stream game has been updated to: Just Chatting" in e.arguments[0]:
            if gv.on_bj and gv.user_blackjack is None:
                off_auto(self)

            elif gv.on_bj and gv.user_blackjack is not None:
                gv.bj_off_automat = True

        elif "The stream game has been updated to: Food & Drink" in e.arguments[0]:
            if gv.on_bj and gv.user_blackjack is None:
                off_auto(self)

            elif gv.on_bj and gv.user_blackjack is not None:
                gv.bj_off_automat = True

        elif "The stream game has been updated to: Travel & Outdoors" in e.arguments[0]:
            if gv.on_bj and gv.user_blackjack is None:
                off_auto(self)

            elif gv.on_bj and gv.user_blackjack is not None:
                gv.bj_off_automat = True

        # On
        elif "The stream game has been updated to: " in e.arguments[0] and not gv.on_bj:
            on_auto(self)

        # Vons for chatters
        if time() > gv.time_points:
            points_chat()

        # Penalty blackjack
        if gv.user_blackjack is not None and time() > gv.pen_blackjack:
            pen_blackjack(self, gv.user_blackjack, gv.bet_blackjack)

        # Verify if the chatter is a sub
        if tags["subscriber"] == "1" and tags["display-name"] not in gv.all_subs \
                and tags["display-name"] not in gv.no_vons:

            user = tags["display-name"]
            if user in gv.all_plebs:
                gv.all_plebs.remove(user)
            gv.all_subs.append(user)


        # Verify if the chatter isn't a sub
        elif tags["subscriber"] == "0" and tags["display-name"] not in gv.all_plebs \
                and tags["display-name"] not in gv.no_vons:

            user = tags["display-name"]
            if user in gv.all_subs:
                gv.all_subs.remove(user)
            gv.all_plebs.append(user)

        # Global commands
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]

            # Verify how many Vons have the user
            if cmd == "vons":
                user = tags["display-name"]
                try:
                    other_user = e.arguments[0].split()
                    other_user = other_user[1]
                except:
                    other_user = None
                points_user(self, user, other_user)

            # Blackjack when a round has already started
            elif gv.user_blackjack == tags["display-name"] and cmd == "bj" and gv.on_bj:
                try:
                    temp = e.arguments[0].split()
                    gv.choice_blackjack = temp[1]
                except:
                    pass
                blackjack(self, gv.choice_blackjack, gv.user_blackjack, gv.bet_blackjack)


            # Blackjack chen a round hasn't already started
            elif cmd == "bj" and gv.user_blackjack is None and gv.on_bj:
                gv.user_blackjack = tags["display-name"]
                try:
                    temp = e.arguments[0].split()
                    gv.choice_blackjack = temp[1]
                    gv.bet_blackjack = temp[2]
                except:
                    gv.bet_blackjack = None
                blackjack(self, gv.choice_blackjack, gv.user_blackjack, gv.bet_blackjack)


            # Roulette
            # If the user is a mod, he can't play roulette because he can't be timed out
            elif cmd == "roulette" and tags["mod"] != "1" and gv.on_roulette:
                player = tags["display-name"]
                if tags["subscriber"] == "1":
                    sub = True
                else:
                    sub = False
                roulette(self, player, sub)


        # MODS only commands
        if e.arguments[0][:1] == '!' and (tags["mod"] == "1" or tags["display-name"].lower() == gv.owner):
            cmd = e.arguments[0].split(' ')[0][1:]
            mod = tags["display-name"]

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

            # Minigames on
            elif cmd == "on":
                try:
                    minigame = e.arguments[0].split()
                    minigame = minigame[1]
                except:
                    minigame = None
                on(self, mod, minigame)


            # Minigames off
            elif cmd == "off" and gv.user_blackjack is None:
                try:
                    minigame = e.arguments[0].split()
                    minigame = minigame[1]
                except:
                    minigame = None
                off(self, mod, minigame)
