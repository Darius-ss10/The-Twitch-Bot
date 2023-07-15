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
    if time() >= gv.time_flower and len(gv.all) > 1:

        # Access the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # All users that have already received at least one flower are being extracted from the database, if they haven't been already
        if gv.all_flower == []:
            for row in cursor.execute('''SELECT username FROM Flowers'''):
                gv.all_flower.append(row[0])

        # Number of flowers
        nr_flowers = random.randint(1, 3)

        # Receiver
        receiver = None
        while (receiver is None or receiver == user):
            nr_receiver = random.randint(0, len(gv.all) - 1)
            receiver = gv.all[nr_receiver]

        # The receiver has already received at least one flower
        if receiver in gv.all_flower:
            # Access the receiver's number of flowers
            cursor.execute('''SELECT flowers FROM Flowers WHERE username = ?''', (receiver,))
            temp = cursor.fetchone()[0] + nr_flowers

            # The receiver receives his flowers
            cursor.execute('''UPDATE Flowers SET flowers = ? WHERE username = ?''', (temp, receiver))

        # The receiver hasn't yet received flowers
        else:
            # The receiver receives his flowers
            cursor.execute('''INSERT INTO Flowers (username, flowers) VALUES (?, ?)''', (receiver, nr_flowers))
            gv.all_flower.append(receiver)

        # Save and close the database
        conn.commit()
        conn.close()

        if (nr_flowers == 1):
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
