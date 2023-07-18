# Imports
from time import time


# Global variables
def initialize():
    # Variables for the owner of the channel and the bot
    # Indicates the streamer's username
    global owner
    owner = ""  # Here you have to put the channel the bot will connect to
    owner = owner.lower()

    # Indicates the streamer's ID
    global owner_id
    owner_id = None  # Here the streamer's ID will be automatically put

    # Indicates the bot's username
    global bot_username
    bot_username = ""  # Here you have to put the bot's username
    bot_username = bot_username.lower()

    # Indicates the bot's ID
    global bot_id
    bot_id = None  # Here the bot's ID will be automatically put

    # Indicates the bot's OATH token
    global bot_OATH_token
    bot_OATH_token = ""  # Here you have to put the OATH token of the bot

    # Indicates the bot's user access token
    global bot_access_token
    bot_access_token = None  # Here the user access token of the bot will be automatically put

    # Indicates the bot's client ID
    global bot_client_id
    bot_client_id = ""  # Here you have to put the client ID of the bot

    # Indicates the bot's client secret
    global bot_client_secret
    bot_client_secret = ""  # Here you have to put the client secret of the bot


    # Variables for Vons
    # Indicates the moment when all chatters will receive some Vons
    global time_points
    time_points = time() + 600

    # Indicates all users that have sent at least one message in the last X minutes
    global chat
    chat = []

    # Indicates all users that have sent al least one message from the beginning of the stream
    global all
    all = []

    # Indicates all users from the database
    global data
    data = []

    # All subs
    global all_subs
    all_subs = []

    # All plebs
    global all_plebs
    all_plebs = []

    # Indicates the names of the bots who will never receive Vons
    global no_vons
    no_vons = ['Nightbot', 'StreamElements']


    # Variables games on/off
    # Indicates if the blackjack minigame if on or off
    global on_bj
    on_bj = False

    # Indicates if the roulette's on or off
    global on_roulette
    on_roulette = True

    # Indicates if the rock, paper, scissors minigame is on or off
    global on_rps
    on_rps = True


    # Variable for auto on/off blackjack when the streamer opens/closes a game
    # Auto on/off blackjack
    global bj_off_auto
    bj_off_auto = False


    # Variables for the roulette minigame
    # Indicates the time when the roulette will be available
    global time_roulette
    time_roulette = time()

    # Indicates the roulette's prize
    global roulette_prize
    roulette_prize = 1000


    # Variables for blackjack
    # Indicates the moment when the blackjack will be available
    global time_blackjack
    time_blackjack = time()

    # Indicates the moment when the blackjack penalty will be applied (if needed)
    global pen_blackjack
    pen_blackjack = time()

    # Indicates the user that plays the blackjack round
    global user_blackjack
    user_blackjack = None

    # Indicates the user's choice
    global choice_blackjack
    choice_blackjack = None

    # Indicates the user's bet
    global bet_blackjack
    bet_blackjack = None

    # Indicates if the blackjack round has started or not
    global flag_start_blackjack
    flag_start_blackjack = False

    # Indicates if the card is an A or not
    global flag_as_blackjack
    flag_as_blackjack = False

    # Indicates if we have to verify the player's number of Vons
    global flag_points_blackjack
    flag_points_blackjack = True

    # Indicates the player's number of Vons
    global points_temp_blackjack
    points_temp_blackjack = None

    # Indicates the sum of user's cards
    global total_blackjack
    total_blackjack = 0

    # Indicates the sum of bot's cards
    global total_blackjack_bot
    total_blackjack_bot = 0

    # Indicates bot's cards
    global cards_blackjack_bot
    cards_blackjack_bot = []

    global cards_blackjack_bot_final
    cards_blackjack_bot_final = ""


    # Variables for the rock, paper, scissors minigame
    # Indicates the moment when the game will be available
    global time_rps
    time_rps = time()

    # Indicates the moment when the penalty will take place (if needed)
    global pen_rps
    pen_rps = time()

    # Indicates the user which plays the game
    global user_rps
    user_rps = None

    # Indicates the user's choice
    global choice_rps
    choice_rps = None

    # Indicates the user's bet
    global bet_rps
    bet_rps = None

    # Indicates if we have to check the player's number of Vons
    global flag_points_rps
    flag_points_rps = True

    # Indicates how many Vons have the user which plays the game
    global points_temp_rps
    points_temp_rps = None


    # Variables for loto
    # Indicates the winner number
    global number_loto
    number_loto = None

    # Indicates the loto prize
    global prize_loto
    prize_loto = None


    # Variable for the grinch command
    # Indicates the moment when the grinch command will be available
    global time_grinch
    time_grinch = time()


    # Variables for the give flowers command
    # Indicates when the command will be available
    global time_flower
    time_flower = time()

    # Indicates all the users that have already received at least one flower
    global all_flower
    all_flower = []


    # Variable for wise command
    # Indicates when the wise command will be available
    global time_wise
    time_wise = time()


    # Indicates the moment when the messages with infos about Vons and commands will be sent
    global time_help
    time_help = time() + 1800
