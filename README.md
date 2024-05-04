# mostpp-mailing-bot

![License](https://img.shields.io/github/license/GregoryKogan/mostpp-mailing-bot)
[![Hits-of-Code](https://hitsofcode.com/github/GregoryKogan/mostpp-mailing-bot?branch=main)](https://hitsofcode.com/github/GregoryKogan/mostpp-mailing-bot/view?branch=main)

This bot obtains registration information by reading notification emails in your inbox. Subsequently, you can view the data of those who registered, send them confirmation letters or thanks for their participation.

### Environment variables

`.env` file should be created in the root directory with the following variables:

- `EMAIL_ADDRESS`: Email address to send emails from
- `EMAIL_APP_PASSWORD`: App password for the email address
- `NOTIFIER_ADDRESS`: Email address to receive notifications from
- `DUMP_EMAIL_ADDRESS`: Email address to send all emails to in DEV mode
- `BOT_TOKEN`: Telegram bot token
- `ALLOWED_USERS`: String of comma-separated list of allowed users
- `DEVELOPER_CHAT_ID`: Chat ID of the developer

Example:

```shell
EMAIL_ADDRESS=john.doe@mail.ru
EMAIL_APP_PASSWORD=123ABC123ABC
NOTIFIER_ADDRESS=notifier@organization.com
DUMP_EMAIL_ADDRESS=jane.doe@mail.ru
BOT_TOKEN=12312313123:ABCABCABCABC
ALLOWED_USERS="123456789,987654321"
DEVELOPER_CHAT_ID=123456789
```

### Configuration

Configuration is done in `src/config.py` file.
The most important setting is `MODE` which can be either `DEV` or `PROD`. In `DEV` mode, all emails are sent to `DUMP_EMAIL_ADDRESS` and in `PROD` mode, the bot sends emails to the actual recipients.

### Running the bot

```shell
docker compose build
docker compose up -d
```

Container will be started in detached mode. It's configured to always restart on failure. So to stop the bot, use

```shell
docker stop mostpp-bot
docker rm mostpp-bot
```
