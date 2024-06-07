import email
from email.header import decode_header
import imaplib
from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging


class EmailReadingClient:
    def __init__(self, address: str, password: str, imap_server: str) -> None:
        self.address = address
        self.password = password
        self.imap_server = imap_server
        self.imap = imaplib.IMAP4_SSL(self.imap_server)

        self.login()

    def __del__(self) -> None:
        self.imap.logout()

    def login(self) -> None:
        logging.info(f"Logging in to {self.imap_server} as {self.address}")
        login_response = self.imap.login(self.address, self.password)
        if login_response[0] != "OK":
            raise ValueError(f"Login failed: {login_response}")

    def get_messages_from_last_n_month_from_sender(
        self, months_ago: int, sender: str
    ) -> list:
        logging.info(f"Getting messages from last {months_ago} months from {sender}")
        uids = self.get_email_uids_from_last_n_months(months_ago)
        messages = [self.read_email(uid) for uid in uids]
        return self.filter_by_sender(messages, sender)

    def get_email_uids_from_last_n_months(self, months_ago: int) -> list[str]:
        self.imap.select("INBOX")

        date_n_months_ago = datetime.now() - relativedelta(months=months_ago)
        formatted_date_n_months_ago = date_n_months_ago.strftime("%d-%b-%Y")

        return list(
            reversed(
                self.imap.uid(
                    "search", None, f'(SINCE "{formatted_date_n_months_ago}")'
                )[1][0].split()
            )
        )

    def read_email(self, uid: str):
        res, msg_bytes = self.imap.uid("fetch", uid, "(RFC822)")
        if res != "OK":
            raise ValueError(f"Failed to read email with uid({uid}): {res}")
        return email.message_from_bytes(msg_bytes[0][1])

    def filter_by_sender(self, messages: list, sender: str) -> list:
        return [
            message
            for message in messages
            if sender.lower() in EmailReadingClient.get_sender(message).lower()
        ]

    @staticmethod
    def get_sender(message) -> str:
        decoded_header = decode_header(message["From"])[0]
        if isinstance(decoded_header[0], bytes):
            return decoded_header[0].decode(decoded_header[1])
        else:
            return decoded_header[0]

    @staticmethod
    def get_subject(message) -> str:
        decoded_header = decode_header(message["Subject"])[0]
        if isinstance(decoded_header[0], bytes):
            return decoded_header[0].decode(decoded_header[1])
        else:
            return decoded_header[0]

    @staticmethod
    def get_plain_text_body(message) -> str:
        return "".join(
            part.get_payload(decode=True).decode("utf-8")
            for part in message.walk()
            if (
                part.get_content_maintype() == "text"
                and part.get_content_subtype() == "plain"
            )
        )
