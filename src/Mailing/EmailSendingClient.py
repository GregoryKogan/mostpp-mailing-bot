import smtplib, ssl, imaplib, email
import time
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
        for recipient in mailing_list:
            self.send_email(recipient, content)

    def send_email(self, to: str, content: EmailContent) -> None:
        msg = EmailMessage()
        msg["Subject"] = content.subject
        msg["From"] = self.address
        msg["To"] = to if config.MODE == "PROD" else self.address
        msg.set_content(content.body)

        if errors := self.smtp.send_message(msg):
            # TODO: log errors
            raise RuntimeError(errors)

        self.imap.append(
            self.get_sent_folder_name(),
            "\\Seen",
            imaplib.Time2Internaldate(time.time()),
            msg.as_string().encode("utf8"),
        )

    def get_sent_folder_name(self):
        _, mailing_list = self.imap.list()
        for box in mailing_list:
            decoded_box = box.decode("utf-8")
            if "Sent" in decoded_box:
                return decoded_box.split()[-1].strip('"')
        raise RuntimeError("Sent folder not found")
