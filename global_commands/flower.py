# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
import os
import sqlite3
from cooldown import cooldown


# Locate the database
DATABASE = os.path.abspath("base.db")


# Give flower
def flower(self, user):
    c = self.connection

    # The command when there's no cooldown
    if time() >= gv.time_flower and len(gv.chat) > 1:

        # Access the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Number of flowers
        nr_flowers = random.randint(1, 3)

        # Receiver
        receiver = None
        while (receiver is None or receiver == user):
            nr_receiver = random.randint(0, len(gv.chat) - 1)
            receiver = gv.chat[nr_receiver]

        # Check if the receiver has already received flowers
        cursor.execute('''SELECT flowers FROM Flowers WHERE username = ?''', (receiver,))
        existing_receiver = cursor.fetchone()

        if existing_receiver:
            # The receiver has already received at least one flower
            temp = existing_receiver[0] + nr_flowers

            # The receiver receives his flowers
            cursor.execute('''UPDATE Flowers SET flowers = ? WHERE username = ?''', (temp, receiver))

        else:
            # The receiver hasn't yet received flowers
            cursor.execute('''INSERT INTO Flowers (username, flowers) VALUES (?, ?)''', (receiver, nr_flowers))

        # Save and close the database
        conn.commit()
        conn.close()

        if nr_flowers == 1:
            message = f"{receiver} received {nr_flowers} flower from {user}."
        else:
            message = f"{receiver} received {nr_flowers} flowers from {user}."

        c.privmsg(self.channel, message)

        # Here you can change the cooldown for this command
        gv.time_flower = time() + 120

    # The command when there's an active cooldown
    elif time() < gv.time_flower:
        time_left = int(gv.time_flower - time())
        info = "the next flower."
        c.privmsg(self.channel, cooldown(time_left, user, info))

    # There aren't enough users in the chat
    else:
        message = f"{user}, there aren't enough users in the chat to offer flowers to."
        c.privmsg(self.channel, message)


# Top 10 flower
def top_10_flower(self):
    c = self.connection

    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    top_10 = []
    for row in cursor.execute('''SELECT * FROM Flowers ORDER BY flowers DESC LIMIT 10'''):
        top_10.append(row)

    for i in range(len(top_10)):
        message = f"{i+1}. {top_10[i][0]} with {top_10[i][1]} flower(s)."
        c.privmsg(self.channel, message)
