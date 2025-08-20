import os
from dotenv import load_dotenv
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

load_dotenv()


def send_email(sender, receiver, email):
    smtp = {"server": "smtp.gmail.com", "port": 587}

    message = MIMEText(email["content"], "plain", "utf-8")
    message["From"] = sender["username"]
    message["To"] = receiver["username"]
    message["Subject"] = Header(email["subject"], "utf-8")

    try:
        with SMTP(smtp["server"], smtp["port"]) as server:
            server.starttls()
            server.login(sender["username"], sender["password"])
            server.sendmail(sender["username"], receiver["username"], message.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Email sending failed: {str(e)}")


if __name__ == "__main__":
    sender = {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")}
    if not sender["username"] or not sender["password"]:
        print("Error: Please set USERNAME and PASSWORD in the .env file")
        exit(1)

    receiver = {"username": input("Receiver: ").strip()}
    email = {"subject": input("Subject: ").strip(), "content": input("Content: ").strip()}
    send_email(sender, receiver, email)
