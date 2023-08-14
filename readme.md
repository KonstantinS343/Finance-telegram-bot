# 📊 Finance Control Telegram Bot

[![Tests](https://github.com/KonstantinS343/Finance-telegram-bot/actions/workflows/ci.yaml/badge.svg)](https://github.com/KonstantinS343/Finance-telegram-bot/actions/workflows/ci.yaml)
[![Security](https://github.com/KonstantinS343/Notes/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/KonstantinS343/Notes/actions/workflows/github-code-scanning/codeql)
[![GitHub license](https://img.shields.io/github/license/range-of-motion/budget.svg)](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/LICENSE)

Manage your finances with ease with the help of the telegram bot **Finance Control**! This bot provides you with convenient tools for creating personalized categories, adding income 💰 and expenses 💸, as well as viewing reports in the form of tables 📊 and pie charts 📈.

## Main functions

📌 **Create Categories:** Personalize your financial system by creating your own categories for expenses and income. This will help you analyze your finances in more detail.

💰 **Adding income and expenses:** Just send the bot information about your financial transactions. Don't miss a single transaction!

📊 **Reports and Analysis:** Get clear reports on the state of your finances. View the data in the form of convenient tables and visual pie charts. This will help you better understand where your money is going and how to increase your income.

🌐 **Language change:** Now you can choose a convenient interface language. Russian 🇷🇺, Belarusian 🇧🇾 and English 🇬🇧 languages are available to make interaction with the bot as comfortable as possible.

## How to get started

1. **Launching the bot**: After clicking on the `start` button, we are   greeted with a greeting and a button panel appears to control the bot.
![Start](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/images/start.gif)

2. **Create categories:**  Use the appropriate buttons to create/delete personalized categories.
![Categories](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/images/categoris.gif)

3. **Add operations:** Send the bot information about your income 💰 and expenses 💸 using the appropriate buttons. Specify the amount and select the appropriate category.
![Money](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/images/money.gif)

4. **Change the language:** Select a convenient interface language using the settings button (there is also reference information there). Now you can interact with the bot in your preferred language.
![Settings](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/images/settings.gif)

5. **Get reports:** Use the `/report` command to get reports on your finances. View data in the form of tables 📊 and pie charts 📈 to better manage your budget.
![Report](https://github.com/KonstantinS343/Finance-telegram-bot/blob/main/images/report.gif)

## Customization

### Environment

In the `src` folder, create the file 📜 `.env` and fill it in according to the template:

```dosini
TELEGRAM=439854958493:rkjgnrngrjgnrjgjrbgjrrjrJJe # Your bot token

HOST=db # The host of your database (locally localhost, and db in docker)
POSTGRES_DB=postgres # Name of your database
POSTGRES_USER=postgres # Password of your database
POSTGRES_PASSWORD=postgres # Username from your database
PORT=5432 # Database port

DB_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres # Url of the main database

DEBUG=0 # If 0, then DEBUG mode is disabled

REDIS_HOST=redis # The host of your redis database (locally localhost, and redis in docker)
REDIS_PORT=6379 # Redis port

SMTP_HOST=smtp.gmail.com # The host of your smtp client
SMTP_PORT=465  # The port of your smtp client

SMTP_USER=example@gmail.com # Your mail for sending emails
SMTP_PASSWORD=jkrdbglrbgriugb # Email password

CELERY_HOST=redis # Celery host for broker(locally localhost, and redis in docker)
CELERY_PORT=6379/1 # Celery port
```

### Preparation

In the `src` folder, create the `reports` and `diagrams` folders for reports.

And run this command:

```sh
export PYTHONPATH=path_to_project:$PYTHONPATH
```

Instead `path_to_project` use the path to the project.

### Launch

#### On-site launch

At the root of the project in 1 terminal:

```sh
python3.10 -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt

cd alembic/
alembic upgrade head

cd ..
python src/main.py
```

In the `src' folder in terminal 2:

```sh
celery -A celery_app:celery worker --loglevel=INFO 
```

#### In docker

At the root of the project:

```docker
docker compose up
```

## Tech used

- [Aiogram](https://docs.aiogram.dev/en/latest/) ⚡
- [Redis](https://redis.io/)  🚀
- [PostgreSQL](https://www.postgresql.org/)  🐘
- [SQLAlchemy](https://www.sqlalchemy.org/)  🧪
- [Celery](https://docs.celeryq.dev/en/stable/) 🖥
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) ⚗️
- [Docker](https://www.docker.com/) 📦
- [Babel](https://babel.pocoo.org/en/latest/) 🌐

## License

This Telegram bot is open source and available under the [MIT License](LICENCE).
