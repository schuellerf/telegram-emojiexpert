# Telegram Emoji Expert Bot
<img src="/pics/screenshot_search.png" alt="Search for the Bot" title="Search for the Bot" width="20%" />
<img src="/pics/screenshot_demo.png" alt="Use the Bot" title="Use the Bot" width="20%" />

Please send this bot _single Emojis_ and it will show the official "unicode name"!

This also works for all those skin tones and other special Emojis I wasn't able to find out what they mean.

btw. this Bot also know _all_ normal "unicode" characters...

## Usage
Just open up Telegram and search for **@emojiexpert_bot** or **Emoji Expert** and start sending _single_ Emojis

**YOU SHOULD NOT NEED TO DO ANYTHING BELOW**

## Installation
You can also host the bot yourself

**Talk to @BotFather on Telegram**
- Type `/start` to start a conversation with the bot father.
- Type `/newbot` and follow the instructions to create our own bot.
- Remember the access token - you will need it later.
- You may configure your bot by setting a name or picture.

**Configure your linux server**

```sh
# Create a special user for the bot
sudo adduser telegram --gecos "" --disabled-password

# Install required packages with the package manager
sudo apt install python3-requests

# OR install Python 3 and dependecies with pip
# use this only if you have problems with the commandline above...
#sudo apt install python3 python3-pip
#sudo python3 -m pip install requests --upgrade
```

**Download and install Telegram Emoji Expert**

```sh
# Change to the created user
su telegram
cd ~

git clone https://github.com/schuellerf/telegram-emojiexpert.git
cd telegram-emojiexpert
cp config.template.py config.py

# Edit the config file with your favorit editor
vim config.py
```

## Usage
Start the program with
```
python3 emojiexpert.py
```

To keep your new telegram bot running when you logout you might want to checkout [tmux](https://tmux.github.io/), which is probably shipped with your favorite distribution.

