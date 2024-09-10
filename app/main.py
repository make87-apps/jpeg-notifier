from datetime import datetime, timedelta

import requests
from make87 import get_topic, topic_names
from make87_messages.image.ImageJPEG_pb2 import ImageJPEG

cooldown = 30  # seconds
last_sent_time = datetime.min


def send_notification_with_image(image_data: bytes):
    global last_sent_time
    current_time = datetime.now()

    if current_time < last_sent_time + timedelta(seconds=cooldown):
        print("Cooldown in effect, skipping notification.")
        return

    # Send the notification
    response = requests.post(
        "https://ntfy.sh/make87",
        data=image_data,  # "image_data".encode("utf-8"),  # Message body
        headers={
            "Title": "New Image Notification",
            "Tags": "skull",
            "Filename": "suspect.jpg",
        },
    )

    if response.ok:
        print("Notification sent successfully.")
        last_sent_time = current_time
    else:
        print(f"Failed to send notification: {response.reason}")


def main():
    topic = get_topic(name=topic_names.IMAGE_DATA)

    def callback(message: ImageJPEG):
        image_data = message.data
        send_notification_with_image(image_data)

    topic.subscribe(callback)


if __name__ == "__main__":
    main()
