# Imports
import irc.bot
import global_variables as gv

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

        # Information about the user
        tags = {}
        for i in range(len(e.tags)):
            tags[e.tags[i]["key"]] = e.tags[i]["value"]

        # Global commands
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]


        # MODS only commands
        if e.arguments[0][:1] == '!' and (tags["mod"] == "1" or tags["display-name"].lower() == gv.owner):
            cmd = e.arguments[0].split(' ')[0][1:]
            mod = tags["display-name"]
            print(f"Command: {cmd} | Mod: {mod}")