# Imports
import sys
sys.path.append("..")
import random
import global_variables as gv
from points import mods_points


# Loto
def mods_loto(self, nr_min, nr_max, prize, mod):
    c = self.connection

    # The command hasn't been misspelled
    if nr_min and nr_max and prize:
        # The prize cannot be a negative number of Vons
        if int(prize) < 0:
            message = f"{mod}, you can't set the prize as a negative number of Vons."
            c.privmsg(self.channel, message)

            return

        # The prize cannot be 0 Vons
        elif int(prize) == 0:
            message = f"{mod}, you can't set the prize to 0 Vons."
            c.privmsg(self.channel, message)

            return

        nr_1 = int(nr_min)
        nr_2 = int(nr_max)
        prize = int(prize)

        # The winner number is chosen
        gv.number_loto = random.randint(nr_1, nr_2)

        message = f"The loto round has started! The user which will guess the winner number between {nr_min} and " \
                  f"{nr_max} will receive {prize:n} Vons!"
        c.privmsg(self.channel, message)

    # The command has been misspelled
    else:
        message = f"{mod}, you have misspelled the command. You should have written: !loto nr_min nr_max prize"
        c.privmsg(self.channel, message)


# When somebody guesses the winner number
def win_loto(self, player):
    c = self.connection

    message = f"{player} have guessed {gv.number_loto}  and will receive {gv.prize_loto:n} Vons!"
    c.privmsg(self.channel, message)

    mods_points(self, None, player, gv.prize_loto)

    gv.number_loto = None
    gv.prize_loto = None
