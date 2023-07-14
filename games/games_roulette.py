# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
from cooldown import cooldown
from points import mods_points
from timeout import timeout


# Russian roulette game
def roulette(self, player, sub):
    c = self.connection

    # The player is a sub
    if sub:

        # There's no cooldown
        if time() >= gv.time_roulette:
            num = random.randint(1, 10)

            # The player won
            if num % 2 == 0:
                if gv.roulette_prize == 1000:
                    message = f"{player} tries the roulette. {player} survived and will receive 1k Vons. The prize is still 1k."

                else:
                    message = f"{player} tries the roulette. {player} survived and will receive {gv.roulette_prize // 1000}k Vons. " \
                              f"The prize has been decreased to 1k."

                c.privmsg(self.channel, message)

                mods_points(self, None, player, gv.roulette_prize)

                # The prize is being decreased to 1k
                gv.roulette_prize = 1000


            # The playser lost
            else:
                gv.roulette_prize += 1000
                message = f"{player} tries the roulette. {player} hasn't survived but will be back among us in 90 seconds. " \
                          f"The prize has been increased at {gv.roulette_prize // 1000}k Vons."
                c.privmsg(self.channel, message)

                timeout(player, 90, "You lost the roulette.")

            # Here you can change the roulette's cooldown
            gv.time_roulette = time() + 180

        # The case where's an active cooldown
        elif time() < gv.time_roulette:
            time_left = int(gv.time_roulette - time())
            info = "the next roulette."

            c.privmsg(self.channel, cooldown(time_left, player, info))

    # The user isn't a sub
    else:
        message = f"{player}, !roulette is a sub only command."
        c.privmsg(self.channel, message)
