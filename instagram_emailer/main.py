from dotenv import dotenv_values
from instagrapi import Client


def get_unread_messages(client: Client):
    threads = client.direct_threads(selected_filter="unread")
    for thread in threads:
        sender = thread.inviter.full_name if thread.inviter else thread.thread_title
        for message in thread.messages:
            if not message.is_sent_by_viewer:
                print(f"{sender}: {message.text}")
                print()


def main():
    config = dotenv_values(".env")

    client = Client()
    client.login(config["USERNAME"], config["PASSWORD"])

    get_unread_messages(client)


if __name__ == "__main__":
    main()
