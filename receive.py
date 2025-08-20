from imaplib import IMAP4_SSL
from email import message_from_bytes
from email.header import decode_header
from dotenv import load_dotenv
import os

load_dotenv()


def decode_email_header(header):
    decoded_header = decode_header(header)
    return "".join([str(t[0], t[1] or "utf-8") if isinstance(t[0], bytes) else t[0] for t in decoded_header])


def receive_email(credential):
    imap = {"server": "imap.gmail.com", "port": 993}

    try:
        mail = IMAP4_SSL(imap["server"], imap["port"])
        mail.login(credential["username"], credential["password"])
        mail.select("INBOX")

        _, id_list = mail.search(None, "ALL")
        latest_id = id_list[0].split()[-1]
        _, msg_data = mail.fetch(latest_id, "(RFC822)")
        body = msg_data[0][1]
        message = message_from_bytes(body)

        print(f"Sender: {message['from']}")
        print(f"Subject: {decode_email_header(message['subject'])}")
        print(f"Date: {message['date']}")

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Content:", body)
                    break
        else:
            body = message.get_payload(decode=True).decode()
            print("Content:", body)

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Receive email failed: {str(e)}")


if __name__ == "__main__":
    credential = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }
    if not credential["username"] or not credential["password"]:
        print("Error: Please set USERNAME and PASSWORD in the .env file")
        exit(1)
    receive_email(credential)
