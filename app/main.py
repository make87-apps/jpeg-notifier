import logging
from datetime import datetime, timedelta

import requests
from make87 import initialize, get_subscriber, resolve_topic_name
from make87_messages.image.compressed.image_jpeg_pb2 import ImageJPEG

cooldown = 30  # seconds
last_sent_time = datetime.min


def send_notification_with_image(image_data: bytes):
    global last_sent_time
    current_time = datetime.now()

    if current_time < last_sent_time + timedelta(seconds=cooldown):
        logging.info("Cooldown in effect, skipping notification.")
        return

    # Send the notification
    response = requests.post(
        "https://ntfy.sh/make87",
        data=image_data,  # Message body
        headers={
            "Title": "New Image Notification",
            "Tags": "skull",
            "Filename": "suspect.jpg",
        },
    )

    if response.ok:
        logging.info("Notification sent successfully.")
        last_sent_time = current_time
    else:
        logging.error(f"Failed to send notification: {response.reason}")


def main():
    initialize()
    topic_name = resolve_topic_name(name="IMAGE_DATA")
    topic = get_subscriber(name=topic_name, message_type=ImageJPEG)

    def callback(message: ImageJPEG):
        image_data = message.data
        send_notification_with_image(image_data)

    topic.subscribe(callback)


if __name__ == "__main__":
    main()
