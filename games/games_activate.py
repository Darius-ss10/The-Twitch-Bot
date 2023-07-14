# Imports
import sys
sys.path.append("..")
import global_variables as gv
from time import time


# Blackjack on auto
def on_auto(self):
    c = self.connection

    gv.time_blackjack = time()
    gv.on_bj = True

    message = "@chat, the blackjack is on."
    c.privmsg(self.channel, message)


# Blackjack off auto
def off_auto(self):
    c = self.connection

    gv.on_bj = False
    gv.bj_off_auto = False

    message = "@chat, the blackjack is off."
    c.privmsg(self.channel, message)


# Mini-games on
def on(self, mod, minigame):
    c = self.connection

    # The command without a minigame
    if minigame is None:
        message = f"{mod}, you haven't chosen which minigame you want to start. Ex : !on bj"

    # The command with a minigame
    else:
        # Blackjack when it's off
        if minigame == "bj" and not gv.on_bj:
            gv.on_bj = True
            gv.time_blackjack = time()
            message = f"{mod}, you have turned on the blackjack."

        # Blackjack when it's on
        elif minigame == "bj":
            message = f"{mod}, the blackjack is already on."


        # Roulette when it's off
        elif minigame == "roulette" and not gv.on_roulette:
            gv.on_roulette = True
            gv.time_roulette = time()
            message = f"{mod}, you have started the roulette."

        # Roulette when it's on
        elif minigame == "roulette":
            message = f"{mod}, the roulette is already on."

        # Minigame that doesn't exist
        else:
            message = f"{mod}, you wanted to start a minigame we don't have yet or you misspelled the command."

    c.privmsg(self.channel, message)


# Mini-games off
def off(self, mod, minigame):
    c = self.connection

    # The command without a minigame
    if minigame is None:
        message = f"{mod}, you haven't chosen a minigame to stop. Ex : !off bj"

    # The command with a minigame
    else:
        # Blackjack when it's on
        if minigame == "bj" and gv.on_bj:
            gv.on_bj = False
            message = f"{mod}, you have stopped the blackjack."

        # Blackjack when it's off
        elif minigame == "bj":
            message = f"{mod}, the blackjack is already off."

        # Roulette when it's on
        elif minigame == "roulette" and gv.on_roulette:
            gv.on_roulette = False
            message = f"{mod}, you have turned off the roulette."

        # Roulette when it's off
        elif minigame == "roulette":
            message = f"{mod}, the roulette is already turned off."

        # Minigame that doesn't exist
        else:
            message = f"{mod}, you wanted to stop a minigame we don't have yet or you misspelled the command."

    c.privmsg(self.channel, message)
