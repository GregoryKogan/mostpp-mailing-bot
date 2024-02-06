from dotenv import load_dotenv
import os
from EventManager import EventManager, EmailClient


def main():
    email_client = EmailClient(
        os.environ.get("EMAIL_ADDRESS"),
        os.environ.get("EMAIL_APP_PASSWORD"),
        "imap.mail.ru",
    )

    event_manager = EventManager(email_client, os.environ.get("NOTIFIER_ADDRESS"))
    for r in event_manager.get_registrations():
        print(r.__dict__)


if __name__ == "__main__":
    load_dotenv(verbose=True, override=True)
    main()
