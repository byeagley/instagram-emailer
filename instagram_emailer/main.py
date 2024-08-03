"""Send unread Instagram messages to an email address."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from instagrapi import Client

EMAIL_SUBJECT = "Unread Instagram Messages"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 465


def send_gmail(
    subject: str, content: str, *, sender: str, recipient: str, gmail_password: str
) -> None:
    """Send an email using Gmail SMTP server.

    Parameters
    ----------
    subject : str
        The subject of the email.
    content : str
        The content of the email.
    sender : str
        The email address of the sender.
    recipient : str
        The email address of the recipient.
    gmail_password : str
        The app password generated for the Gmail account.
    """
    email_message = EmailMessage()
    email_message.set_content(content)
    email_message["Subject"] = subject
    email_message["From"] = sender
    email_message["To"] = recipient

    with smtplib.SMTP_SSL(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as smtp_server:
        smtp_server.login(sender, gmail_password)
        smtp_server.sendmail(sender, recipient, email_message.as_string())


def get_unread_messages(client: Client) -> str | None:
    """Get unread messages from Instagram direct threads.

    Parameters
    ----------
    client : Client
        An instance of the Client class from the instagrapy package.

    Returns
    -------
    str or None
        A string containing unread messages from Instagram direct threads.
        If there are no unread messages, return None.
    """
    unread_messages = ""

    threads = client.direct_threads(selected_filter="unread", thread_message_limit=20)
    if not threads:
        return None

    for thread in threads:
        sender = thread.users[0].username if thread.users else thread.thread_title
        unread_messages += f"{sender}:\n"

        for message in thread.messages:
            if message.is_sent_by_viewer:
                continue

            if message.text:
                unread_messages += f"{message.text}\n"
            else:
                unread_messages += f"[Media: {message.item_type}]\n"
        unread_messages += "\n\n"

    return unread_messages


def main():
    email_address = os.getenv("EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    instagram_username = os.getenv("INSTAGRAM_USERNAME")
    instagram_password = os.getenv("INSTAGRAM_PASSWORD")

    if not email_address or not gmail_password:
        err = "Email address and Gmail app password are required in .env file"
        raise ValueError(err)

    client = Client()
    client.login(instagram_username, instagram_password)

    unread_messages = get_unread_messages(client)
    if not unread_messages:
        return

    send_gmail(
        EMAIL_SUBJECT,
        unread_messages,
        sender=email_address,
        recipient=email_address,
        gmail_password=gmail_password,
    )


if __name__ == "__main__":
    main()
