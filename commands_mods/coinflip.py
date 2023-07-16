# Imports
import random
import sys
sys.path.append("..")
import os
import sqlite3
from timeout import timeout
import global_variables as gv


# Locate the database
DATABASE = os.path.abspath("base.db")


# Coinflip
def mods_coinflip(self, user, mod):
    c = self.connection

    if user and user[0] == '@':
        user = user[1:]

    # Command + tag to a user
    if user is not None:
        num = random.randint(1, 2)

        # VIP
        if num % 2 == 0:
            message = f"{user} wants to play. The result of the coinflip was heads, so he wins a VIP."
            c.privmsg(self.channel, message)

            # Access the database
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Check if the table is empty
            cursor.execute("SELECT COUNT(*) FROM VIPS")
            result = cursor.fetchone()

            if result[0] > 0:
                # Last VIP
                for row in cursor.execute('''SELECT username FROM VIPS ORDER BY id DESC LIMIT 1'''):
                    last_vip = row[0]
                    message = f"{gv.owner}, {last_vip} was the last VIP."
                    c.privmsg(self.channel, message)

            # The most recent VIP is saved in the database
            cursor.execute('''INSERT INTO VIPS (username) VALUES (?)''', (user,))

            # Save and close the database
            conn.commit()
            conn.close()

        # Timeout
        else:
            message = f"{user} wants to play. The result of the coinflip was tails, so he'll get a timeout."
            c.privmsg(self.channel, message)

            timeout(user, 86400, "You lost the coinflip.")

    # Command without a tag
    else:
        message = f"{mod}, you have to tag the person who wants to play."
        c.privmsg(self.channel, message)
