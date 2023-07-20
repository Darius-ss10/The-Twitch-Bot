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
7. Register an application for the bot on the [Twitch Dev console](https://dev.twitch.tv/console/apps/create).
   You can name your application as you want, it doesn't really matter.
   You can set the OAuth Redirect URL to "http://localhost:3000".
   (It will help us later to get an authorization code)
   You can set the Category to "Chat Bot".
   After you've created the application, you'll be able to see the Client ID and the Client Secret. 
   (We'll need them later)
8. Generate your OAuth token.
   You can use [this website](https://twitchapps.com/tmi/) to generate your OAuth token.
   You'll have to log in with your bot's account. 
   The token will look like this: "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx".
   What's important to save is the part after "oauth:".
   (We'll need it later)
9. Complete the file _global_variables.py_.
   You'll have to replace the values of the variables with the values you got in the previous steps:
   - _owner_ at line 10: put the Twitch channel the bot will connect to
   - _bot_username_ at line 19: put the name of your bot's account
   - _bot_OATH_token_ at line 28: put the OAuth token you got in step 8
   - _bot_client_id_ at line 36: put the Client ID you got in step 7
   - _bot_client_secret_ at line 40: put the Client Secret you got in step 7
10. The most tricky step: Generate an authorization code.
    Go to this link :
    https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=<your_client_id>&redirect_uri=http://localhost:3000&scope=moderator%3Amanage%3Abanned_users
    (replace <your_client_id> with your bot's Client ID).
    A Twitch popup will appear and ask you to log in with your bot's account (if you're not already logged in.).
    After that, you'll have to grant permission (i.e. click on the "Authorize" button).
    Then, you'll be redirected to a page with a URL like this:
    http://localhost:3000/?code=<your_authorization_code>&scope=moderator%3Amanage%3Abanned_users
    Finally, you'll have to copy the value of the parameter "code"
    in the URL (i.e. <your_authorization_code>) and paste it in the file _global_variables.py_ at line 44.
11. Run the file _get_refresh_token_first_time_use.py_.
    You can do it by right-clicking on the file and then clicking on "Run 'get_refresh_token_first_time_use'"
    if you use PyCharm as your IDE.
    If you use another IDE,
    you can run the file
    by running the following command in the terminal: ```python3 /path/to/get_refresh_token_first_time_use.py```
    (Be aware that the authorization code you got in step 10 is usable only once, and it's used in this step. 
    So, if for some reason (e.g. your refresh token is no longer valid) you have to run this step again, you'll have to generate a new authorization code.)

## How to run the bot
Run the file _TwitchBot.py_.
You can do it by right-clicking on the file and then clicking on "Run 'TwitchBot'" if you use PyCharm as your IDE.
If you use another IDE,
you can run the file by running the following command in the terminal: ```python3 /path/to/TwitcBot.py```

## Description of the bot
The bot has 3 main features:
- It can read the chat and respond to some commands
- It can send messages in the chat
- It can time out users

This bot has an economy system that allows users to earn Vons (the currency of the bot)
by watching the stream and to bet them by playing games.<br />
The accepted commands are:
- !commands = show all the commands
- !help = information about Vons
- !vons = show how many Vons you have
- !love = random love message (e.g. !love @user)
- !bj = blackjack (e.g. !bj start 1000 or !bj start all)
- !rps = rock, paper, scissors (e.g. !rps rock 2000 or !rps rock all)
- !roulette = Russian roulette 
- !wise = how wise the chatters were today 
- !grinch = subs can steal Vons from plebs
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


## Description of some commands