from dotenv import dotenv_values
from instagrapi import Client


def get_unread_messages(client: Client) -> str:
    unread_messages = ""

    threads = client.direct_threads(selected_filter="unread", thread_message_limit=20)
    for thread in threads:
        sender = thread.users[0].username if thread.users else thread.thread_title
        unread_messages += f"Last few messages from {sender}:\n"

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
    config = dotenv_values(".env")

    client = Client()
    client.login(config["USERNAME"], config["PASSWORD"])

    unread_messages = get_unread_messages(client)
    print(unread_messages)



if __name__ == "__main__":
    main()
