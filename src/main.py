from dotenv import load_dotenv
import os
import imaplib


def main():
    username = "grisha.koganovskiy@mail.ru"
    password = os.environ.get("EMAIL_APP_PASSWORD")
    imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)

    imap.login(username, password)

    imap.select("INBOX")
    emails_uids = imap.uid("search", "ALL")[1][0].split()
    for emails_uid in emails_uids:
        email_data = imap.uid("fetch", emails_uid, "(RFC822)")[1][0][1]
        print(email_data.decode("utf-8"))
        break


if __name__ == "__main__":
    load_dotenv()
    main()
