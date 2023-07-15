# Imports
import random


# Random love %
def love(self, pers1, pers2):
    c = self.connection

    # Command + tag to another person
    if pers2 is not None:
        percent = random.randint(0, 100)
        message = f"{pers1} and {pers2} are in love at {percent}%."

    # Command without a tag
    else:
        message = f"{pers1}, you have to tag somebody."

    c.privmsg(self.channel, message)
