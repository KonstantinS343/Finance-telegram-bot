# Setting up the environment
    cd Finance-telegram-bot
    poetry shell
    poetry install

# Pre-launch preparation
### 1. Telegram settings

To get a telegram bot token, you need to contact the [BotFather](https://t.me/BotFather), after creation he will give you a token.

### 2. Set the enviroment variable
    cd Finance-telegram-bot/core/config
    true > .env
    nano .env 
Insert your telegram token in the format `TELEGRAM=your_telegram_token`, after saving the file `Ctrl+S` and exiting `Ctrl+X`.

### 3.Database initialization
    sudo apt install sqlite3 
    sqlite3 finance.db < createdb.sql

# Project launch
    poetry run start

# Tech used

* [Poetry](https://python-poetry.org/) for more convenient package management
* [aiogram](https://aiogram.dev/) for write the bot itself
* [aiohttp](https://docs.aiohttp.org/en/stable/) for requests
* [asyncio](https://docs.python.org/3/library/asyncio.html) for asynchronous programming
# License

This Telegram bot is open source and available under the [MIT License](LICENCE).

