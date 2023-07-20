# The Twitch Bot
This is a Twitch chatbot made in Python
that can help you to bring some fun to your stream chat and make it more interactive.
It will also help you to keep your chat alive while your playing games ;)

## First steps to use the bot 
#### It will seem long, but it's not that hard, and you'll have to do it only once. I promise it will be worth it.
#### However, if you have any questions or if you want a custom Twitch Bot, feel free to contact me. This is my Discord username: **mrdada_**
1. Download the bot from the repository
2. Make sure you have Python 3.10 or higher installed on your computer 
(All my tests were made with Python 3.10, so I can't guarantee that it will work with older versions)
3. Install an IDE.
   It will help you to run the bot and to make changes to it (it will make all the process less scary 
than using the terminal).
   I strongly recommend [PyCharm](https://www.jetbrains.com/pycharm/download/) because it simplifies
the process of installing packages, and it has a lot of useful features.
   Don't worry, you can use the free Community Edition.
4. Install the required packages.
   If you use PyCharm as your IDE, the process of installing the required packages will be 
easy as the IDE will propose you to install the packages by itself.
   If you use another IDE, you can install the
required packages by running the following command in the terminal:
```pip install -r /path/to/requirements.txt``` (you'll of course have to install pip first if you don't have it yet in 
order to run this command)
5. Create a Twitch account for your bot.
   I don't recommend using your main account for the bot because it will be easier
to manage the bot if it has its own account, and it will be less weird when the bot will send messages in chat.
6. Activate the 2FA on your bot's account.
   It will allow you to register an application for the bot on the Twitch Dev console.
   You can activate the 2FA on the bot's account [here](https://www.twitch.tv/settings/security).
7. Register an application for the bot on the [Twitch Dev console](https://dev.twitch.tv/console/apps/create).<br />
   You can name your application as you want, it doesn't really matter.<br />
   Set the OAuth Redirect URL to "http://localhost:3000".
   (It will help us later to get an authorization code)<br />
   Set the Category to "Chat Bot".<br />
   After you've created the application, you'll be able to see the bot's Client ID and the bot's Client Secret. 
   (We'll need them later)
8. Generate the bot's OAuth token.
   You can use [this website](https://twitchapps.com/tmi/) to generate your bot's OAuth token.
   You'll have to log in with your bot's account. 
   The token will look like this: "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx".
   What's important to save is the part after "oauth:".
   (We'll need it later)
9. Fill the gaps in the file _global_variables.py_.
   You'll have to replace the values of the variables with the values
   (all those values should be placed into quotes) you got in the previous steps:
   - _owner_ at line 10: put the name of the Twitch channel the bot will connect to
   - _bot_username_ at line 19: put the name of your bot's account
   - _bot_OATH_token_ at line 28: put the OAuth token you got in step 8
   - _bot_client_id_ at line 36: put the Client ID you got in step 7
   - _bot_client_secret_ at line 40: put the Client Secret you got in step 7
10. The most tricky step: Generate an authorization code.
    Go to this link :
    https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=<your_client_id>&redirect_uri=http://localhost:3000&scope=moderator%3Amanage%3Abanned_users
    (replace <your_client_id> with your bot's Client ID).
    A Twitch popup will appear and ask you to log in with your bot's account (if you're not already logged in.).
    After that, you'll have to grant permission (i.e. click on the "Authorize" button).<br />
    Then, you'll be redirected to a page with a URL like this:
    http://localhost:3000/?code=<your_authorization_code>&scope=moderator%3Amanage%3Abanned_users <br />
    Finally, you'll have to copy the value of the parameter "code"
    in the URL (i.e. <your_authorization_code>) and paste it in the file _global_variables.py_ at line 44.
11. Run the file _get_refresh_token_first_time_use.py_.
    You can do it by right-clicking on the file and then clicking on "Run 'get_refresh_token_first_time_use'"
    if you use PyCharm as your IDE.
    If you use another IDE,
    you can run the file
    by running the following command in the terminal: ```python3 /path/to/get_refresh_token_first_time_use.py```
    (Be aware that the authorization code you got in step 10 is usable only once, and it's used in this step. 
    So, if for some reason (e.g. your refresh token is no longer valid) you have to do this step again, you'll have to generate a new authorization code.)

## How to run the bot
Run the file _TwitchBot.py_.
You can do it by right-clicking on the file and then clicking on "Run 'TwitchBot'" if you use PyCharm as your IDE.
If you use another IDE,
you can run the file by running the following command in the terminal: ```python3 /path/to/TwitchBot.py```

## Description of the bot
The bot has 3 main features:
- It can read the chat and respond to some commands
- It can send messages in the chat
- It can time out users

This bot has an economy system that allows users to earn Vons (the currency of the bot)
by being active in the stream's chat and to bet them by playing games.<br />
The accepted commands are:
- !commands = show all the commands
- !help = show information about Vons
- !vons = show how many Vons you have
- !love = random love percentage between 2 users (e.g. !love @user)
- !bj = blackjack (e.g. !bj start 1000 or !bj start all)
- !rps = rock, paper, scissors (e.g. !rps rock 2000 or !rps rock all)
- !roulette = Russian roulette 
- !wise = how wise the chatters were today 
- !grinch = subs can steal Vons from plebs (aka non-subs)
- !flower = give flowers to a random person in chat

MODS only commands:
- !coinflip = coinflip when a user asks or redeems for it(e.g. !coinflip @user)
- !loto = loto game (e.g. !loto nr_min nr_max prize) (!loto 1 50 10000)
- !g = change stream category on Twitch (e.g. !g tft)
- !topflower = top 10 people who have the most flowers
- !give_vons = give Vons to chatters (e.g. !give_vons @user 1000 or !give_vons all 1000)
- !on = turn on a minigame (e.g. !on bj)
- !off = turn off a minigame (e.g. !off bj) (minigames = bj, rps, roulette)
- !reset = reset a table from the database (e.g. !reset table) (tables = vons, flowers, vips)


## Description of some commands and how I've designed them
### Minigames: 
All the minigames (bj, rps, roulette) are turned on by default except for the blackjack because for this 
one, there are several messages that the bot can send in the chat, 
and it can be annoying for the viewers if the streamer is doing Just Chatting.<br />
The blackjack minigame turns on automatically 
when the streamer starts playing a game and turns off automatically when the streamer goes back to Just Chatting.
(The bot analyzes StreamElements'
messages to know when the streamer starts playing a game and when he goes back to Just Chatting, 
so this automatic feature will work only if you use StreamElements' bot in your channel)<br />
All the minigames can be turned on/off by the streamer or the mods.<br />
Each minigame has a different cooldown.<br />
If there's a draw in the rock, paper, scissors game, and the user doesn't replay, he'll lose his bet. 
If a user stops randomly in the middle of a blackjack game, he'll lose his bet.

### Roulette: 
The roulette is a Russian roulette.
The starting prize is 1000 Vons, and it increases by 1000 Vons each time
someone loses.
If the user loses, he'll get a timeout of 3 minutes, and if he wins, he'll get the prize.
(And the prize goes back to 1000 Vons)<br />
This minigame is a subs only one.
Maybe it will make more people subscribe to the channel ;)

### Wise: 
If the user was at least 70% wise, he'll win 5000 Vons and if he wasn't, he'll lose 1000 Vons.

### Flower: 
You can use this command to create a competition between the viewers.
(Idea: the user who has the most flowers at the end of each month wins a prize)

### Coinflip: 
You can create a redeem with Channel Points on Twitch (just one per day, so it will make it more special), 
and the user who redeems it will be able to play the coinflip. 
If the result is heads, he'll win a VIP that will last until there will be another user who'll win the coinflip, 
and if it's tails, he'll get a 24h timeout.

### Loto: 
You can create a redeem with Channel Points on Twitch, and each time a user redeems it,
a mod (or the streamer) will have to run the !loto command.
A random number between nr_min and nr_max will be generated,
and the chatter who'll guess it will win the prize.

### G: 
You can use this command to change the stream's category on Twitch. 
I've added this command because I wanted to add a simpler way to change the category of the stream on Twitch.
In order to make this command work, you'll have to have StreamElements' bot in your channel.<br />
I've already added some categories, but you can add more if you want. 
You'll just have to add them in the file _category.py_ that you'll find in the folder _commands_mods_.
The dictionary _categories_ that you can find at line 6 in that file has the following structure: 
{"abbreviation": "the message the bot will send in chat"}. 
For instance,
if you want to change the stream's category directly in the Twitch chat to Just Chatting by using StreamElements' bot, 
instead of typing "!game Just Chatting", 
you'll only have to type "!g jc".


## Ideas for what you can do with the Vons
You could allow your viewers to redeem their Vons for a permanent VIP if they have enough Vons (like 3M Vons or something like that).


## ENJOY!