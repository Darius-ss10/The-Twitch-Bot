# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
from cooldown import cooldown
from points import mods_points, points_user_helper


# Rock, paper, scissors minigame
def rps(self, choice, user, bet):
    c = self.connection

    choices = ["rock", "paper", "scissors"]

    # The command when there's no cooldown
    if time() >= gv.time_rps:
        # Verify if the command hasn't been misspelled
        if bet != "all":
            try:
                bet = int(bet)
                gv.bet_rps = bet
            except:
                bet = None

        if bet != "all" and bet:
            if bet == 0:
                message = f"{user}, you can't bet 0 Vons."
                c.privmsg(self.channel, message)
                gv.user_rps = None
                gv.choice_rps = None
                gv.bet_rps = None
                return

            elif bet < 0:
                message = f"{user}, you can't bet a negative number of Vons."
                c.privmsg(self.channel, message)
                gv.user_rps = None
                gv.choice_rps = None
                gv.bet_rps = None
                return

        if choice is None or bet is None:
            message = f"{user}, you have misspelled the command. A correct example is: !rps rock 1000"
            gv.user_rps = None
            gv.choice_rps = None
            gv.bet_rps = None
            c.privmsg(self.channel, message)

        elif choice not in choices:
            message = f"{user}, the only possible choices are : rock, paper or scissors."
            gv.user_rps = None
            gv.choice_rps = None
            gv.bet_rps = None
            c.privmsg(self.channel, message)

        # The command hasn't been misspelled
        else:
            choice = choice.lower()

            # Verify how many Vons the user has
            if gv.flag_points_rps:
                gv.points_temp_rps = points_user_helper(user)

                if bet == "all":
                    bet = int(gv.points_temp_rps)
                    gv.bet_rps = bet

                    if gv.bet_rps == 0:
                        message = f"{user}, you can't play the game because you have 0 Vons."
                        c.privmsg(self.channel, message)

                        # The game reinitialized
                        gv.user_rps = None
                        gv.choice_rps = None
                        gv.bet_rps = None
                        gv.flag_points_rps = True
                        gv.points_temp_rps = None

                        return

            # The user wants to bet more Vons that he actually has
            if int(bet) > int(gv.points_temp_rps):
                message = f"{user}, you don't have enough Vons to bet {bet:n}."
                c.privmsg(self.channel, message)

                # The game reinitialized
                gv.user_rps = None
                gv.choice_rps = None
                gv.bet_rps = None
                gv.flag_points_rps = True
                gv.points_temp_rps = None

            # The bet is accepted
            else:
                # The bet is placed
                if gv.flag_points_rps:
                    mods_points(self, None, user, -gv.bet_rps)
                    gv.flag_points_rps = False

                # The bot makes his choice
                choice_bot = random.randint(0, 2)
                choice_bot = choices[choice_bot]

                # Draw
                if choice == choice_bot:
                    message = f"{user}, you have chosen {choice} and the bot has chosen that too. Replay the game fast " \
                              f"if you don't want to lose by disqualification."

                    gv.pen_rps = time() + 30

                # The user won
                elif (choice == "rock" and choice_bot == "scissors") \
                        or (choice == "paper" and choice_bot == "rock") \
                        or (choice == "scissors" and choice_bot == "paper"):

                    message = f"{user}, you have chosen {choice} and the bot has chosen {choice_bot}. Congrats, you " \
                              f"have doubled your bet of {gv.bet_rps:n} Vons."

                    mods_points(self, None, user, gv.bet_rps * 2)

                    # Here you can change the cooldown of the rock, paper, scissors minigame
                    # The game reinitialized
                    gv.time_rps = time() + 300
                    gv.pen_rps = time()
                    gv.user_rps = None
                    gv.choice_rps = None
                    gv.bet_rps = None
                    gv.flag_points_rps = True
                    gv.points_temp_rps = None

                # The user lost
                elif (choice_bot == "rock" and choice == "scissors") \
                        or (choice_bot == "paper" and choice == "rock") \
                        or (choice_bot == "scissors" and choice == "paper"):

                    message = f"{user}, you have chosen {choice} and the bot has chosen {choice_bot}. You have lost " \
                              f"your bet of {gv.bet_rps:n} Vons."

                    # Here you can change the cooldown of the rock, paper, scissors minigame
                    # The game reinitialized
                    gv.time_rps = time() + 300
                    gv.pen_rps = time()
                    gv.user_rps = None
                    gv.choice_rps = None
                    gv.bet_rps = None
                    gv.flag_points_rps = True
                    gv.points_temp_rps = None

                c.privmsg(self.channel, message)

    # The command when there's a cooldown
    elif time() < gv.time_rps:
        time_left = int(gv.time_rps - time())
        info = "the next game of rock, paper, scissors."

        gv.user_rps = None
        gv.choice_rps = None
        gv.bet_rps = None
        c.privmsg(self.channel, cooldown(time_left, user, info))


# Penalty for the rock, paper, scissors minigame
def pen_rps(self, user, bet):
    c = self.connection

    message = f"{user}, you have waited too much time to replay the last game, so that means you have been disqualified " \
              f"and you have lost your bet of {bet:n} Vons."
    c.privmsg(self.channel, message)

    # Here you can change the cooldown of the rock, paper, scissors minigame
    # The game reinitialized
    gv.time_rps = time() + 300
    gv.pen_rps = time()
    gv.user_rps = None
    gv.choice_rps = None
    gv.bet_rps = None
    gv.flag_points_rps = True
    gv.points_temp_rps = None
