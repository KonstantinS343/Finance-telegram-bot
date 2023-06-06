# Setting up the environment
    cd Finance-telegram-bot
    poetry shell
    poetry install

# Telegram and Weather settings
To get a telegram bot token, you need to contact the [BotFather](https://t.me/BotFather), after creation he will give you a token.

# Set the enviroment variable
    cd Finance-telegram-bot/core/config
    true > .env
    nano .env 
Insert your telegram token in the format `TELEGRAM=your_telegram_token`, after saving the file `Ctrl+S` and exiting `Ctrl+X`.


# Project launch
    poetry run start

# Tech used

* [Poetry](https://python-poetry.org/) for more convenient package management
* [aiogram](https://aiogram.dev/) for write the bot itself
* [aiohttp](https://docs.aiohttp.org/en/stable/) for requests
* [asyncio](https://docs.python.org/3/library/asyncio.html) for asynchronous programming
# License

This Telegram bot is open source and available under the [MIT License](LICENCE).

