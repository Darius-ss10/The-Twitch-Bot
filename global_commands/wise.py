# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
from cooldown import cooldown
from points import mods_points, points_user_helper


# How wise the people in chat have been
def wise(self, user):
    c = self.connection

    # The command when there's no cooldown
    if time() >= gv.time_wise:
        percent = random.randint(0, 100)

        if percent >= 70:
            prize = 5000
        else:
            prize = -1000

        mods_points(self, None, user, prize)

        # Here you can change the cooldown of this command
        gv.time_wise = time() + 60

        if percent >= 70:
            message = f"{user}, you have been {percent}% wise. You received {prize:n} Vons. Now you have {points_user_helper(user):n}."
        else:
            prize = prize * -1
            message = f"{user}, you have been {percent}% wise. You have lost {prize:n} Vons. Now you have {points_user_helper(user):n}."

        c.privmsg(self.channel, message)


    # The command when there's an active cooldown
    elif time() < gv.time_wise:
        time_left = int(gv.time_wise - time())
        info = "the next try."

        c.privmsg(self.channel, cooldown(time_left, user, info))
