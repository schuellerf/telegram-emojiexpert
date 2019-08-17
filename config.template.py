# Rename this file to config.py and insert your token and password

# Name of the Telgram bot (ending with 'bot', without leading '@')
NAME = "emojiexpert_bot"

# Token of your Telegram bot (Given to you by @BotFather)
TOKEN = ""

# Initial timeout for retry after ConnectionError from the server
# timeout will be multiplied by 2 every retry to avoid annoing behavior
SERVER_RETRY_TIMEOUT = 10

GREETING = """I'm @{}!

Please send me a single Emoji and I'll tell you the official unicode name of it.

That's it I can't do more... but I should know ALL Emojis \U0001F609

If you have questions go the place where I was born: https://github.com/schuellerf/telegram-emojiexpert.git
""".format(NAME)

# Statement to show additionaly to the help
STATEMENT = "\nIf you like my job please donate any amount to https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=CYYUAJGURTYKE&item_name=emojiexpert&currency_code=EUR&source=url"

# Long polling timeout in seconds
TIMEOUT = 60 * 5

# DO NOT EDIT BELOW THIS LINE
# ===========================
API_URL = "https://api.telegram.org/bot" + TOKEN + "/"
