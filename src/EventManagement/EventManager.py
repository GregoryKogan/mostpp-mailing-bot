import config
import base64

from Mailing.EmailReadingClient import EmailReadingClient
from EventManagement.NotificationScraper import NotificationScraper, RegistrationInfo


class EventManager:
    def __init__(self, email_client: EmailReadingClient, notifier_address: str) -> None:
        self.email_client = email_client
        self.notifier_address = notifier_address

    def get_registrations(self) -> dict[str, list[RegistrationInfo]]:
        messages = self.get_registration_messages()

        records = [
            NotificationScraper(
                EmailReadingClient.get_plain_text_body(message)
            ).scrape()
            for message in messages
        ]

        registrations = {}
        for record in records:
            if record.event not in registrations:
                registrations[record.event] = []
            registrations[record.event].append(record)

        return registrations

    def get_registration_messages(self):
        return [
            message
            for message in self.get_notifier_messages()
            if all(
                keyword in EmailReadingClient.get_subject(message).lower()
                for keyword in config.REGISTRATION_SUBJECT_KEYWORDS
            )
        ]

    def get_notifier_messages(self):
        return self.email_client.get_messages_from_last_n_month_from_sender(
            config.REGISTRATION_PERIOD, self.notifier_address
        )
