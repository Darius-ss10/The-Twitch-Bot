def cooldown(time_left, user, info):
    # When there are more than 60 seconds left
    if time_left >= 60:
        minutes = time_left // 60
        seconds = time_left - minutes * 60

        # When there are several minutes left
        if minutes != 1:
            # Ex: 7 minutes
            if seconds == 0:
                message = f"{user}, come back in {minutes} minutes for {info}"

            # Ex: 7 minutes and 1 second
            elif seconds == 1:
                message = f"{user}, come back in {minutes} minutes and {seconds} second for {info}"

            # Ex: 7 minutes and [2, 59] seconds
            else:
                message = f"{user}, come back in {minutes} minutes and {seconds} seconds for {info}"

        # When there's only 1 minute left
        else:
            # Ex: 1 minute
            if seconds == 0:
                message = f"{user}, come back in {minutes} minute for {info}"

            # Ex: 1 minute and 1 second
            elif seconds == 1:
                message = f"{user}, come back in {minutes} minute and {seconds} second for {info}"

            # Ex: 1 minute and [2, 59] seconds
            else:
                message = f"{user}, come back in {minutes} minute and {seconds} seconds for {info}"

    # When there are less than 60 seconds left
    else:
        # Ex: 1 second
        if time_left == 1:
            message = f"{user}, come back in {time_left} second for {info}"

        # Ex: [2, 59] seconds
        else:
            message = f"{user}, come back in {time_left} seconds for {info}"

    return message
