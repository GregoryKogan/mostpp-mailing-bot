from dataclasses import dataclass

from WebScraping.EventScraper import EventData


@dataclass
class EmailContent:
    subject: str
    body: str


class EmailGenerator:
    def __init__(
        self, event: EventData, email_template: str, subject_template: str
    ) -> None:
        self.event = event
        self.email_template = email_template
        self.subject_template = subject_template

    def generate(self) -> EmailContent:
        subject = self.subject_template.format(
            event_name=self.event.name,
            event_link=self.event.link,
            event_date=self.event.date,
            event_time=self.event.time,
        )
        body = self.email_template.format(
            event_name=self.event.name,
            event_link=self.event.link,
            event_date=self.event.date,
            event_time=self.event.time,
        )
        return EmailContent(subject, body)
