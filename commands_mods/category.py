# Change the stream's category (this will need StreamElements)
def mods_change_category(self, category, mod):
    c = self.connection

    # "abbreviation": "the message the bot will send in chat",
    categories = {"jc" : "!game Just Chatting",
                 "tft" : "!game Teamfight Tactics",
                 "m" : "!game Marbles on Stream",
                 "v" : "!game VALORANT",
                 "cs" : "!game Counter-Strike: Global Offensive",
                 "irl" : "!game Travel & Outdoors",
                 "cook" : "!game Food & Drink",
                 "lol" : "!game League of Legends",
                 "he" : "!game Hercules",
                 "gg" : "!game GeoGuessr",
                 "jk" : "!game Jump King",
                 "medan" : "!game The Dark Pictures Anthology: Man of Medan",
                 "bomb" : "!game Bombergrounds: Battle Royale",
                 "tt" : "!game Tricky Towers",
                 "cod" : "!game Call of Duty: Warzone",
                 "forza": "!game Forza Horizon 5",
                 "raft": "!game Raft",
                 "tavern": "!game Tavern Master",
                 "fort": "!game Fortnite",
                 "mp" : "!game Monopoly Plus"}

    # Command + a category the bot knows
    if category in categories.keys():
        message = categories[category]

    # Command without a category
    elif category is None:
        message = f"{mod}, you have to specify a category."

    # Command + a misspelled category
    elif category not in categories.keys():
        # Tries to find the category that matches the most
        temp = []
        for key, val in categories.items():
            if category[0] == key[0]:
                temp.append((key, val))

        # There was no category to match
        if not temp:
            message = f"{mod}, you misspelled the command or I don't know that category yet."

        # There was found at least one category which matched
        else:
            # There was found only one category which matched
            if len(temp) == 1:
                message = f"{mod}, the closest option is : !g {temp[0][0]} -> {temp[0][1]}"

            # There were found several categories which matched
            else:
                options = [f"!g {item[0]} -> {item[1]}" for item in temp]
                message = f"{mod}, the closest options are: {', '.join(options)}"

    c.privmsg(self.channel, message)
