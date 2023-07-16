# Imports
import sys
sys.path.append("..")
import os
import sqlite3


# Locate the database
DATABASE = os.path.abspath("base.db")


# Reset
def reset(self, mod, reset_table):
    c = self.connection

    if reset_table is not None:

        if reset_table == "flowers" or reset_table == "vons" or reset_table == "vips":
            # Access the database
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Check if the table is empty
            cursor.execute(f"SELECT COUNT(*) FROM {reset_table}")
            result = cursor.fetchone()

            if result[0] > 0:
                # Delete all the rows
                cursor.execute(f"DELETE FROM {reset_table}")
                message = f"{mod}, the table {reset_table} has been reset."

                if reset_table == "vips":
                    # Reset the auto-increment value
                    table_name = "VIPS"
                    update_query = f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}'"
                    cursor.execute(update_query)

            else:
                message = f"{mod}, the table {reset_table} is already empty."

            # Save and close the database
            conn.commit()
            conn.close()

            c.privmsg(self.channel, message)

        else:
            message = f"{mod}, the table {reset_table} doesn't exist."
            c.privmsg(self.channel, message)

    else:
        message = f"{mod}, you have to specify the table you want to reset."
        c.privmsg(self.channel, message)
