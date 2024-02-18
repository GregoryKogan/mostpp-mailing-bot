from dataclasses import dataclass

from WebScraping.EventScraper import EventData


@dataclass
class EmailContent:
    subject: str
    body: str

    def __str__(self) -> str:
        return f"<b>{self.subject}</b>\n\n\n{self.body}"


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


class EventEmailGenerator:
    def __init__(
        self,
        pre_template: str,
        pre_subject_template: str,
        post_template: str,
        post_subject_template: str,
    ) -> None:
        self.pre_template = pre_template
        self.pre_subject_template = pre_subject_template
        self.post_template = post_template
        self.post_subject_template = post_subject_template

    def generate_pre_event_email(self, event: EventData) -> EmailContent:
        return EmailGenerator(
            event, self.pre_template, self.pre_subject_template
        ).generate()

    def generate_post_event_email(self, event: EventData) -> EmailContent:
        return EmailGenerator(
            event, self.post_template, self.post_subject_template
        ).generate()

    @staticmethod
    def read_templates(
        pre_template: str,
        pre_subject_template: str,
        post_template: str,
        post_subject_template: str,
    ) -> list[str]:
        with open(pre_template, "r", encoding="utf-8") as file:
            pre_template = file.read()
        with open(pre_subject_template, "r", encoding="utf-8") as file:
            pre_subject_template = file.read()
        with open(post_template, "r", encoding="utf-8") as file:
            post_template = file.read()
        with open(post_subject_template, "r", encoding="utf-8") as file:
            post_subject_template = file.read()
        return [
            pre_template,
            pre_subject_template,
            post_template,
            post_subject_template,
        ]
