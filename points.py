# Imports
from time import time
import global_variables as gv
import os
import sqlite3

# Locate the database
DATABASE = os.path.abspath("base.db")


# Vons for chatters, which have sent at least one message in the last X minutes
def points_chat():
    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Every user in the chat receives his points
    for user in gv.chat:
        # Check if the user is already in the database
        cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
        existing_user = cursor.fetchone()

        if existing_user:
            # The user is already in the database
            temp = existing_user[0] + 100  # Here you can change the number of Vons he receives

            # The user receives his Vons
            cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, user))
        else:
            # The user isn't in the database, but he's added now
            # Here you can change the number of Vons he receives
            cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (user, 100))

    # Save and close the database
    conn.commit()
    conn.close()

    # Here you can change the cooldown
    gv.chat = []
    gv.all_subs = []
    gv.all_plebs = []
    gv.time_points = time() + 600

# Verify how many Vons have the user
def points_user(self, user, other_user):
    c = self.connection

    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Basic command
    if other_user is None or other_user[0] != '@':

        # Check if the user is already in the database
        cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
        existing_user = cursor.fetchone()

        if existing_user:
            temp = existing_user[0]
        else:
            temp = 0

        message = f"{user}, you have {temp:n} Vons."
        c.privmsg(self.channel, message)

    # Command + tag to another user
    else:
        # In the database, users are saved without the @
        if other_user[0] == '@':
            other_user = other_user[1:]

        # Check if the other user is already in the database
        cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (other_user,))
        existing_other_user = cursor.fetchone()

        if existing_other_user:
            temp = existing_other_user[0]
        else:
            temp = 0

        message = f"{other_user} has {temp:n} Vons."
        c.privmsg(self.channel, message)

    # Close the database
    conn.close()


# Verify how many Vons have the user (helper for the games)
def points_user_helper(user):
    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the user is already in the database
    cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
    existing_user = cursor.fetchone()

    if existing_user:
        temp = existing_user[0]
    else:
        temp = 0

    # Close the database
    conn.close()

    return temp


# Mods can give Vons to users
def mods_points(self, mod, user, nr_points, message_show=False):
    c = self.connection

    # The command isn't misspelled
    if user and nr_points and nr_points != 0:
        if user[0] == '@':
            user = user[1:]

        # Access the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # When a single user receives Vons
        if user != "all":

            # Check if the user is already in the database
            cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
            existing_user = cursor.fetchone()

            if existing_user:
                # Access the user's number of Vons
                temp = existing_user[0] + int(nr_points)

                # If the user received a negative number of Vons and goes below 0, set to 0
                if temp < 0:
                    temp = 0

                # Update the user's Vons
                cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, user))

            else:
                # If the user received a negative number of Vons, set to 0
                if int(nr_points) < 0:
                    nr_points_temp = 0
                else:
                    nr_points_temp = int(nr_points)

                # Insert the user into the database
                cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (user, nr_points_temp))
                temp = nr_points_temp

            # Save and close the database
            conn.commit()
            conn.close()

            if message_show:
                message = f"{user}, you received {nr_points:n} Vons. Now you have {temp:n}."
                c.privmsg(self.channel, message)

        # When all chatters receive Vons
        else:
            # Every chatter receives their Vons
            for chatter in gv.chat:

                # Check if the user is already in the database
                cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (chatter,))
                existing_chatter = cursor.fetchone()

                if existing_chatter:
                    # Access the user's number of Vons
                    temp = existing_chatter[0] + int(nr_points)

                    # If the user received a negative number of Vons and goes below 0, set to 0
                    if temp < 0:
                        temp = 0

                    # Update the user's Vons
                    cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, chatter))

                else:
                    # If the user received a negative number of Vons, set to 0
                    if int(nr_points) < 0:
                        nr_points_temp = 0
                    else:
                        nr_points_temp = int(nr_points)

                    # Insert the user into the database
                    cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (chatter, nr_points_temp))

            # Save and close the database
            conn.commit()
            conn.close()

            if int(nr_points) > 0:
                message = f"Every chatter received {nr_points:n} Vons."
            else:
                message = f"Every chatter lost {nr_points:n} Vons."

            c.privmsg(self.channel, message)

    # The command has been misspelled
    else:
        message = f"{mod}, you have misspelled the command. You should have written: !give_vons user nr_points (whole number)"
        c.privmsg(self.channel, message)

