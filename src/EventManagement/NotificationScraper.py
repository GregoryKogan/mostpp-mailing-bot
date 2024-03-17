from dataclasses import dataclass
import re


@dataclass
class RegistrationInfo:
    timestamp: str
    event: str
    name: str
    phone: str
    email: str
    company: str
    position: str
    comment: str

    def pretty_str(self) -> str:
        string = (
            f"{self.timestamp}\n"
            f"{self.name}, {self.phone}, {self.email}\n"
            f"{self.company}, {self.position}"
        )

        if self.comment:
            string += f"\n> {self.comment}"

        return string


class NotificationScraper:
    def __init__(self, plaintext: str) -> None:
        self.plaintext = plaintext

    def scrape(self) -> RegistrationInfo:
        return RegistrationInfo(
            self.get_timestamp(),
            self.get_event(),
            self.get_name(),
            self.get_phone(),
            self.get_email(),
            self.get_company(),
            self.get_position(),
            self.get_comment(),
        )

    def get_timestamp(self) -> str:
        if match := re.search(
            r"\b(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\b", self.plaintext
        ):
            return match[1]

    def get_event(self) -> str:
        if match := re.search(r'"(.*?)"', self.plaintext, re.DOTALL):
            return match[1].replace("\n", " ").replace("\r", "")

    def get_name(self) -> str:
        if match := re.search(r"Контакты пользователя (.*?),", self.plaintext):
            return match[1]

    def get_phone(self) -> str:
        if match := re.search(r"\+?\d[\d\-\(\) ]{7,}\d", self.plaintext):
            return match[0]

    def get_email(self) -> str:
        if match := re.search(r".+,\s*([\w\.-]+@[\w\.-]+\.\w+)", self.plaintext):
            return match[1]

    def get_company(self) -> str:
        if match := re.search(r"Название компании: (.*)", self.plaintext):
            return match[1].strip()

    def get_position(self) -> str:
        if match := re.search(r"Должность: (.*)", self.plaintext):
            return match[1].strip()

    def get_comment(self) -> str:
        if match := re.search(r"Текст сообщения: (.*)", self.plaintext):
            return match[1].strip()
