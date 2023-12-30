# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
from cooldown import cooldown
from points import mods_points, points_user_helper


# Subs steal Vons from plebs
def grinch(self, user, sub):
    c = self.connection

    # At least one pleb has written in chat
    if len(gv.all_plebs) > 0:

        # The user is a sub
        if sub:

            # The command when there's no cooldown
            if time() >= gv.time_grinch:
                nr_points = random.randint(1000, 2000)
                nr_pleb = random.randint(0, len(gv.all_plebs) - 1)
                pleb = gv.all_plebs[nr_pleb]
                nr_points_stolen = 0

                # Check if the pleb is already in the database
                temp_pleb = points_user_helper(pleb)

                # Access the pleb's number of Vons
                if temp_pleb < nr_points:
                    nr_points_stolen = temp_pleb
                else:
                    nr_points_stolen = nr_points

                # The pleb is losing his points
                mods_points(self, None, pleb, -nr_points_stolen)

                # If no Vons were stolen
                if nr_points_stolen == 0:
                    message = f"{user}, sadly {pleb} protected himself, and you weren't able to steal some Vons from him."

                # If some Vons were stolen
                else:
                    mods_points(self, None, user, nr_points_stolen)
                    message = f"{user}, you have successfully stolen {nr_points_stolen:n} Vons from {pleb}."

                # Here you can change the cooldown for this command
                gv.time_grinch = time() + 300

                c.privmsg(self.channel, message)

            # The command when there's an active cooldown
            elif time() < gv.time_grinch:
                time_left = int(gv.time_grinch - time())
                info = "the next robbery."

                c.privmsg(self.channel, cooldown(time_left, user, info))

        # The user isn't a sub
        else:
            message = f"{user}, !grinch is a subs-only command."
            c.privmsg(self.channel, message)

    else:
        message = f"{user}, unfortunately, there aren't any plebs to steal from yet."
        c.privmsg(self.channel, message)
