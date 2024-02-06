import config
import base64

from EmailClient import EmailClient
from NotificationScraper import NotificationScraper, RegistrationInfo


class EventManager:
    def __init__(self, email_client: EmailClient, notifier_address: str) -> None:
        self.email_client = email_client
        self.notifier_address = notifier_address

    def get_registrations(self) -> list[RegistrationInfo]:
        messages = self.get_registration_messages()

        return [
            NotificationScraper(EmailClient.get_plain_text_body(message)).scrape()
            for message in messages
        ]

    def get_registration_messages(self):
        return [
            message
            for message in self.get_notifier_messages()
            if all(
                keyword in EmailClient.get_subject(message).lower()
                for keyword in config.REGISTRATION_SUBJECT_KEYWORDS
            )
        ]

    def get_notifier_messages(self):
        return self.email_client.get_messages_from_last_n_month_from_sender(
            config.REGISTRATION_PERIOD, self.notifier_address
        )
