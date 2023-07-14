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

    extract_users()

    # Every user in the chat receives his points
    for user in gv.chat:
        # The user is already in the database
        if user in gv.data:

            # Access the user's number of Vons
            cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
            temp = cursor.fetchone()[0] + 100  # Here you can change the number of Vons he receives

            # The user receives his Vons
            cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, user))

        # The user isn't in the database, but he's added now
        else:
            # Here you can change the number of Vons he receives
            cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (user, 100))
            gv.data.append(user)

    # Save and close the database
    conn.commit()
    conn.close()

    # Here you can change the cooldown
    gv.chat = []
    gv.time_points = time() + 600


# Verify how many Vons have the user
def points_user(self, user, other_user):
    c = self.connection

    # Access the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    extract_users()

    # Basic command
    if other_user is None or other_user[0] != '@':

        # The user is already in the database
        if user in gv.data:
            # Access the user's number of Vons
            cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
            temp = cursor.fetchone()[0]

        # The user isn't in the database
        else:
            temp = 0

        message = f"{user}, you have {temp:n} Vons."
        c.privmsg(self.channel, message)

    # Command + tag to another user
    else:
        # In the database, users are saved without the @
        if other_user[0] == '@':
            other_user = other_user[1:]

        # The user is already in the database
        if other_user in gv.data:
            # Access the user's number of Vons
            cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (other_user,))
            temp = cursor.fetchone()[0]

        # The user's isn't in the database
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

    extract_users()

    # The user is already in the database
    if user in gv.data:
        # Access the user's number of Vons
        cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
        temp = cursor.fetchone()[0]

    # The user isn't in the database
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

        extract_users()

        # When a single user receives Vons
        if user != "all":

            # The user is already in the database
            if user in gv.data:
                # Access the user's number of Vons
                cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (user,))
                temp = cursor.fetchone()[0] + int(nr_points)

                # If the user received a negative number of Vons and he goes below 0, in the database it's saved that he has 0 Vons
                if temp < 0:
                    temp = 0

                # The user receives his Vons
                cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, user))

            # The user isn't in the database, and he's introduced now
            else:
                # If the user received a negative number of Vons, in the database it's saved that he has 0 Vons
                if int(nr_points) < 0:
                    nr_points_temp = 0

                # If the user received a positive number of Vons, he receives them
                else:
                    nr_points_temp = int(nr_points)

                # The user receives his Vons
                cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (user, nr_points_temp))
                temp = nr_points_temp
                gv.data.append(user)

            # Save and close the database
            conn.commit()
            conn.close()

            if message_show:
                message = f"{user}, you received {nr_points:n} Vons. Now you have {temp:n}."
                c.privmsg(self.channel, message)

        # When all chatters receive Vons
        else:
            # Every chatter receives his Vons
            for chatter in gv.all:

                # The user is already in the database
                if chatter in gv.data:
                    # Access the user's number of Vons
                    cursor.execute('''SELECT points FROM Vons WHERE username = ?''', (chatter,))
                    temp = cursor.fetchone()[0] + int(nr_points)

                    # If the user received a negative number of Vons and he goes below 0, in the database it's saved that he has 0 Vons
                    if temp < 0:
                        temp = 0

                    # The user receives his Vons
                    cursor.execute('''UPDATE Vons SET points = ? WHERE username = ?''', (temp, chatter))

                # The user isn't in the database, and he's introduced now
                else:
                    # If the user received a negative number of Vons, in the database it's saved that he has 0 Vons
                    if int(nr_points) < 0:
                        nr_points_temp = 0

                    # If the user received a positive number of Vons, he receives them
                    else:
                        nr_points_temp = int(nr_points)

                    # The user receives his points
                    cursor.execute('''INSERT INTO Vons (username, points) VALUES (?, ?)''', (chatter, nr_points_temp))
                    gv.data.append(chatter)

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


def extract_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # All users are being extracted from the database if they haven't been already
    if gv.data == []:
        for row in cursor.execute('''SELECT username FROM Vons'''):
            gv.data.append(row[0])

    conn.close()
