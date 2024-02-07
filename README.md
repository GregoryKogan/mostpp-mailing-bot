# mostpp-mailing-bot

This bot obtains registration information by reading notification emails in your inbox. Subsequently, you can view the data of those who registered, send them confirmation letters or thanks for their participation.

### Environment variables

`.env` file should be created in the root directory with the following variables:

- `EMAIL_ADDRESS`: Email address to send emails from
- `EMAIL_APP_PASSWORD`: App password for the email address
- `NOTIFIER_ADDRESS`: Email address to receive notifications from
- `BOT_TOKEN`: Telegram bot token
- `ALLOWED_USERS`: String of comma-separated list of allowed users

Example:

```shell
EMAIL_ADDRESS=john.doe@mail.ru
EMAIL_APP_PASSWORD=123ABC123ABC
NOTIFIER_ADDRESS=notifier@organization.com
BOT_TOKEN=12312313123:ABCABCABCABC
ALLOWED_USERS="123456789,987654321"
```
