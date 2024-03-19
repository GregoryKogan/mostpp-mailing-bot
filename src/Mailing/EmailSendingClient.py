import smtplib, ssl, imaplib, email
import time
import logging
import os
from email.message import EmailMessage
from EmailGeneration.EmailGeneration import EmailContent
import config


class EmailSendingClient:
    def __init__(
        self,
        address: str,
        password: str,
        smtp_server: str,
        imap_server: str,
    ) -> None:
        self.address = address
        self.password = password
        self.smtp_server = smtp_server
        self.imap_server = imap_server

        self.login()

    def __del__(self) -> None:
        self.smtp.quit()
        self.imap.logout()

    def login(self) -> None:
        context = ssl.create_default_context()
        self.smtp = smtplib.SMTP_SSL(self.smtp_server, context=context)
        self.smtp.login(self.address, self.password)

        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.address, self.password)

    def send_email_to_mailing_list(
        self, mailing_list: list[str], content: EmailContent
    ) -> None:
        chunk_size = 10
        for i in range(0, len(mailing_list), chunk_size):
            msg = self.build_message(content)
            current_chunk = mailing_list[i : i + chunk_size]
            msg["To"] = (
                ", ".join(current_chunk)
                if config.MODE == "PROD"
                else ", ".join(
                    [os.environ.get("DUMP_EMAIL_ADDRESS")] * len(current_chunk)
                )
            )
            self.attempt_sending(msg)

    def send_email(self, to: str, content: EmailContent) -> None:
        msg = self.build_message(content)
        msg["To"] = (
            to if config.MODE == "PROD" else os.environ.get("DUMP_EMAIL_ADDRESS")
        )
        self.attempt_sending(msg)

    def attempt_sending(self, msg):
        logging.info(f"Sending email to {msg['To']}")
        if errors := self.smtp.send_message(msg):
            logging.warning(
                f"Errors occurred while sending email to {msg['To']}: {errors}"
            )
            if config.MODE == "DEV":
                raise RuntimeError(errors)
        else:
            logging.info(f"Email to {msg['To']} sent successfully")

        self.imap.append(
            self.get_sent_folder_name(),
            "\\Seen",
            imaplib.Time2Internaldate(time.time()),
            msg.as_string().encode("utf8"),
        )

    def build_message(self, content):
        msg = EmailMessage()
        msg["Subject"] = content.subject
        msg["From"] = self.address
        msg.set_content(content.body)
        return msg

    def get_sent_folder_name(self):
        _, mailing_list = self.imap.list()
        for box in mailing_list:
            decoded_box = box.decode("utf-8")
            if "Sent" in decoded_box:
                return decoded_box.split()[-1].strip('"')
        raise RuntimeError("Sent folder not found")
