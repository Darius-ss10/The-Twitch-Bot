# Imports
import sys
sys.path.append("..")
import random
from time import time
import global_variables as gv
from cooldown import cooldown
from points import mods_points, points_user_helper


# Blackjack minigame
def blackjack(self, choice, user, bet):
    c = self.connection

    # The command when there's no cooldown
    if time() >= gv.time_blackjack:
        choices = ["start", "+", "1", "11", "stop"]
        cards = ["x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        # Verify if the command hasn't been misspelled
        if bet != "all":
            try:
                bet = int(bet)
                gv.bet_blackjack = bet
            except:
                bet = None

        if bet != "all" and bet:
            if bet == 0:
                message = f"{user}, you can't bet 0 Vons."
                c.privmsg(self.channel, message)
                gv.user_blackjack = None
                gv.choice_blackjack = None
                gv.bet_blackjack = None
                return

            elif bet < 0:
                message = f"{user}, you can't bet a negative number of Vons."
                c.privmsg(self.channel, message)
                gv.user_blackjack = None
                gv.choice_blackjack = None
                gv.bet_blackjack = None
                return

        if choice is None or bet is None:
            message = f"{user}, you have misspelled the command. A correct example to start is : !bj start 1000"
            gv.user_blackjack = None
            gv.choice_blackjack = None
            c.privmsg(self.channel, message)

        elif choice not in choices:
            message = f"{user}, the only accepted choices are : start, +, 1, 11 or stop."
            if not gv.flag_start_blackjack:
                gv.user_blackjack = None
            gv.choice_blackjack = None
            c.privmsg(self.channel, message)

        # The command hasn't been misspelled
        else:
            choice = choice.lower()

            # Verify how many Vons the user has
            if gv.flag_points_blackjack:
                gv.points_temp_blackjack = points_user_helper(user)

                if bet == "all":
                    bet = int(gv.points_temp_blackjack)
                    gv.bet_blackjack = bet

                    if gv.bet_blackjack == 0:
                        message = f"{user}, you can't play blackjack because you have 0 Vons."
                        c.privmsg(self.channel, message)

                        # The game reinitialized
                        gv.user_blackjack = None
                        gv.choice_blackjack = None
                        gv.bet_blackjack = None
                        gv.flag_points_blackjack = True
                        gv.points_temp_blackjack = None

                        return

            # The user wants to bet more Vons that he actually has
            if int(bet) > int(gv.points_temp_blackjack):
                message = f"{user}, you don't have enough Vons to bet {bet:n}."
                c.privmsg(self.channel, message)

                # The game reinitialized
                gv.user_blackjack = None
                gv.choice_blackjack = None
                gv.bet_blackjack = None
                gv.flag_points_blackjack = True
                gv.points_temp_blackjack = None

            # The bet is accepted
            else:
                # The bet is placed
                if gv.flag_points_blackjack:
                    mods_points(self, None, user, -gv.bet_blackjack)
                    gv.flag_points_blackjack = False

                # card 1
                nr_card_1 = random.randint(2, 14)
                card_1 = cards[nr_card_1]

                # The round starts
                if choice == "start" and not gv.flag_start_blackjack:
                    # card 1 bot
                    nr_card_1_bot = random.randint(2, 13)
                    card_1_bot = cards[nr_card_1_bot]
                    gv.cards_blackjack_bot.append(card_1_bot)

                    if nr_card_1_bot >= 2 and nr_card_1_bot <= 10:
                        gv.total_blackjack_bot += nr_card_1_bot

                    elif nr_card_1_bot > 10 and nr_card_1_bot <= 13:
                        gv.total_blackjack_bot += 10

                    # card 2
                    nr_card_2 = random.randint(2, 13)
                    card_2 = cards[nr_card_2]

                    # Analyze the cards and calculate the sum of them
                    if card_1 == "A":
                        if nr_card_2 >= 2 and nr_card_2 <= 10:
                            gv.total_blackjack += nr_card_2

                        elif nr_card_2 > 10 and nr_card_2 <= 13:
                            gv.total_blackjack += 10

                        message = f'{user}, you received a {card_2} and a {card_1}. Write fast "!bj 1" in order to choose ' \
                                  f'As = 1 or "!bj 11" to choose As = 11. The first card of the bot is {card_1_bot}.'

                        gv.flag_as_blackjack = True

                    else:
                        if nr_card_1 >= 2 and nr_card_1 <= 10:
                            gv.total_blackjack += nr_card_1

                        elif nr_card_1 > 10 and nr_card_1 <= 13:
                            gv.total_blackjack += 10

                        if nr_card_2 >= 2 and nr_card_2 <= 10:
                            gv.total_blackjack += nr_card_2

                        elif nr_card_2 > 10 and nr_card_2 <= 13:
                            gv.total_blackjack += 10

                        message = f'{user}, you received a {card_2} and a {card_1}. Total = {gv.total_blackjack}' + \
                                  f'. Write fast "!bj +" in order to receive another card or "!bj stop" to stop.' + \
                                  f' The first card of the bot is {card_1_bot}.'

                    c.privmsg(self.channel, message)

                    # Here you can change the max wait time between inputs of the user
                    gv.pen_blackjack = time() + 30
                    gv.flag_start_blackjack = True


                # The user received an A
                elif (choice == "1" or choice == "11") and gv.flag_as_blackjack and gv.flag_start_blackjack:
                    # Total + 11 if he chose As = 11 or total + 1 if he chose As = 1
                    gv.total_blackjack += int(choice)

                    # The user didn't reach 21
                    if gv.total_blackjack != 21:
                        message = f'{user}, you have chosen As = {choice}. Total = {gv.total_blackjack}. ' \
                                  f'Write fast "!bj +" in order to receive another card or "!bj stop" to stop.'

                        # Here you can change the max wait time between inputs of the user
                        gv.pen_blackjack = time() + 30

                    # The user has reached 21
                    else:
                        # cards + total bot
                        cards_total_bot(cards)

                        # The bot didn't reach 21
                        if gv.total_blackjack_bot != 21:
                            message = f"{user}, you received a {card_1}. Total = {gv.total_blackjack}. You have won " \
                                      f"because the bot reached {gv.total_blackjack_bot}. You have doubled your bet of " \
                                      f"{gv.bet_blackjack:n} Vons. Bot's cards have been : {gv.cards_blackjack_bot_final}."

                            mods_points(self, None, user, gv.bet_blackjack * 2)

                        # The bot reached 21 too
                        else:
                            message = f"{user}, you received a {card_1}. Total = {gv.total_blackjack}. It has ended as " \
                                      f"a draw because the bot also reached {gv.total_blackjack_bot}. You haven't lost " \
                                      f"your bet of {gv.bet_blackjack:n} Vons. Bot's cards have been : {gv.cards_blackjack_bot_final}."

                            mods_points(self, None, user, gv.bet_blackjack)

                        # Here you can change the game's cooldown + the game reinitialized
                        reinitialize()

                    c.privmsg(self.channel, message)
                    gv.flag_as_blackjack = False


                # The user wants another card
                elif choice == "+" and gv.flag_start_blackjack and not gv.flag_as_blackjack:
                    # Analyze of the received card
                    # The user received an A
                    if card_1 == "A":
                        # If total + 11 <= 21, the user can choose between As = 11 and As = 1
                        if gv.total_blackjack + 11 <= 21:
                            message = f'{user}, you received a {card_1}. Write fast "!bj 1" in order to choose As = 1 ' \
                                      f'or "!bj 11" to choose As = 11.'

                            # Indicates that the user received an A
                            gv.flag_as_blackjack = True

                        # If total + 11 > 21, the A is directly interpreted as = 1
                        else:
                            gv.total_blackjack += 1

                            # The user didn't reach 21
                            if gv.total_blackjack != 21:
                                message = f'{user}, you received a {card_1} (=1). Total = {gv.total_blackjack}. ' \
                                          f'Write fast "!bj +" in order to receive another card or "!bj stop" to stop.'

                            # The user reached 21
                            else:
                                # cards + total bot
                                cards_total_bot(cards)

                                # The bot didn't reach 21
                                if gv.total_blackjack_bot != 21:
                                    message = f"{user}, you received a {card_1} (=1). Total = {gv.total_blackjack}. " \
                                              f"You have won because the bot reached {gv.total_blackjack_bot}. You have " \
                                              f"doubled your bet of {gv.bet_blackjack:n} Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."


                                    mods_points(self, None, user, gv.bet_blackjack * 2)

                                # The bot reached 21 too
                                else:
                                    message = f"{user}, you received a {card_1} (=1). Total = {gv.total_blackjack}. " \
                                              f"It has ended as a draw because the bot also reached {gv.total_blackjack_bot}. " \
                                              f"You haven't lost your bet of {gv.bet_blackjack:n} Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."


                                    mods_points(self, None, user, gv.bet_blackjack)

                                # Here you can change the game's cooldown + the game reinitialized
                                reinitialize()

                    # The user didn't receive an A
                    else:
                        # Analyze the received card and calculate the new sum
                        if nr_card_1 >= 2 and nr_card_1 <= 10:
                            gv.total_blackjack += nr_card_1

                        elif nr_card_1 > 10 and nr_card_1 <= 13:
                            gv.total_blackjack += 10

                        # The user didn't reach 21
                        if gv.total_blackjack < 21:
                            message = f'{user}, you received a {card_1}. Total = {gv.total_blackjack}. Write fast ' \
                                      f'"!bj +" in order to receive another card or "!bj stop" to stop.'

                        # The user reached 21
                        elif gv.total_blackjack == 21:
                            # cards + total bot
                            cards_total_bot(cards)

                            # The bot didn't reach 21
                            if gv.total_blackjack_bot != 21:
                                message = f"{user}, you received a {card_1}. Total = {gv.total_blackjack}. You have won " \
                                          f"because the bot reached {gv.total_blackjack_bot}. You have doubled your bet " \
                                          f"of {gv.bet_blackjack:n} Vons. Bot's card have been: {gv.cards_blackjack_bot_final}."


                                mods_points(self, None, user, gv.bet_blackjack * 2)

                            # The bot reached 21 too
                            else:
                                message = f"{user}, you received a {card_1}. Total = {gv.total_blackjack}. It has ended " \
                                          f"as a draw because the bot also reached {gv.total_blackjack_bot}. You haven't " \
                                          f"lost your bet of {gv.bet_blackjack:n} Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."


                                mods_points(self, None, user, gv.bet_blackjack)

                            # Here you can change the game's cooldown + the game reinitialized
                            reinitialize()

                        # The user overpassed 21
                        elif gv.total_blackjack > 21:
                            message = f"{user}, you received a {card_1}. Total = {gv.total_blackjack}. You have lost " \
                                      f"because you overpassed 21. You have lost your bet of {gv.bet_blackjack:n} Vons."

                            # Here you can change the game's cooldown + the game reinitialized
                            reinitialize()

                    c.privmsg(self.channel, message)

                    # Here you can change the max wait time between inputs of the user
                    gv.pen_blackjack = time() + 30


                # The user stops the round
                elif choice == "stop" and gv.flag_start_blackjack and not gv.flag_as_blackjack:
                    # cards + total bot
                    cards_total_bot(cards)

                    # The bot obtained less than the user or overpassed 21
                    if gv.total_blackjack_bot < gv.total_blackjack or gv.total_blackjack_bot > 21:
                        message = f"{user}, you have stopped the round at {gv.total_blackjack}. You have won because the " \
                                  f"bot obtained {gv.total_blackjack_bot}. You have doubled your bet of {gv.bet_blackjack:n} " \
                                  f"Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."


                        mods_points(self, None, user, gv.bet_blackjack * 2)

                    # Draw
                    elif gv.total_blackjack_bot == gv.total_blackjack:
                        message =  f"{user}, you have stopped the round at {gv.total_blackjack}. It has ended as a draw " \
                                   f"because the bot also obtained {gv.total_blackjack_bot}. You haven't lost your bet " \
                                   f"of {gv.bet_blackjack:n} Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."


                        mods_points(self, None, user, gv.bet_blackjack)

                    # The bot obtained more than the user without overpassing 21
                    elif gv.total_blackjack_bot > gv.total_blackjack and gv.total_blackjack_bot <= 21:
                        message = f"{user}, you have stopped the round at {gv.total_blackjack}. You have lost because " \
                                  f"the bot obtained {gv.total_blackjack_bot}. You have lost your bet of {gv.bet_blackjack:n} " \
                                  f"Vons. Bot's cards have been: {gv.cards_blackjack_bot_final}."

                    # Here you can change the game's cooldown + the game reinitialized
                    reinitialize()

                    c.privmsg(self.channel, message)

                    # Here you can change the max wait time between inputs of the user
                    gv.pen_blackjack = time() + 30


                # The command has been partially misspelled
                else:
                    # When a round hasn't been started, the only command which is accepted is "!bj start"
                    if not gv.flag_start_blackjack:
                        message = f'{user}, at this moment the only command which is accepted is: "!bj start".'

                        gv.user_blackjack = None
                        gv.choice_blackjack = None
                        gv.bet_blackjack = None

                    # When the user received an A and has the possibility to choose between As = 1 and As = 11
                    # The only commands which are accepted are: "!bj 1" and "!bj 11"
                    elif gv.flag_as_blackjack:
                        message = f'{user}, at this moment the only commands which are accepted are: "!bj 1" or "!bj 11".'

                    # When the user received a card that isn't an A, the only commands which are accepted are: "!bj +" or "!bj stop"
                    elif not gv.flag_as_blackjack:
                        message = f'{user}, at this moment the only commands which are accepted are: "!bj +" or "!bj stop".'

                    c.privmsg(self.channel, message)

    # The command when there's an active cooldown
    elif time() < gv.time_blackjack:
        time_left = int(gv.time_blackjack - time())
        info = "the next blackjack round."

        gv.user_blackjack = None
        gv.choice_blackjack = None
        gv.bet_blackjack = None
        c.privmsg(self.channel, cooldown(time_left, user, info))


# Penalty blackjack
def pen_blackjack(self, user, bet):
    c = self.connection

    message = f"{user}, you have waited too long which means you have been disqualified and you have lost your bet of {bet:n} Vons."
    c.privmsg(self.channel, message)

    # Here you can change the game's cooldown + the game reinitialized
    reinitialize()


# Cards + total bot
def cards_total_bot(cards):
    # Calculate the bot's total
    while gv.total_blackjack_bot < 17:
        nr_card_x_bot = random.randint(2, 14)
        card_x_bot = cards[nr_card_x_bot]
        gv.cards_blackjack_bot.append(card_x_bot)

        if card_x_bot == "A":
            if gv.total_blackjack_bot + 11 <= 21:
                gv.total_blackjack_bot += 11
            else:
                gv.total_blackjack_bot += 1

        else:
            if nr_card_x_bot >= 2 and nr_card_x_bot <= 10:
                gv.total_blackjack_bot += nr_card_x_bot

            elif nr_card_x_bot > 10 and nr_card_x_bot <= 13:
                gv.total_blackjack_bot += 10

    # All bot's cards
    for i in range(len(gv.cards_blackjack_bot)):
        if i == len(gv.cards_blackjack_bot) - 1:
            gv.cards_blackjack_bot_final += "and " + gv.cards_blackjack_bot[i]
        elif i == len(gv.cards_blackjack_bot) - 2:
            gv.cards_blackjack_bot_final += gv.cards_blackjack_bot[i] + " "
        else:
            gv.cards_blackjack_bot_final += gv.cards_blackjack_bot[i] + ", "


# The game reinitialized
def reinitialize():
    gv.time_blackjack = time() + 300
    gv.user_blackjack = None
    gv.choice_blackjack = None
    gv.bet_blackjack = None
    gv.flag_points_blackjack = True
    gv.flag_start_blackjack = False
    gv.flag_as_blackjack = False
    gv.points_temp_blackjack = None
    gv.total_blackjack = 0
    gv.total_blackjack_bot = 0
    gv.cards_blackjack_bot = []
    gv.cards_blackjack_bot_final = ""