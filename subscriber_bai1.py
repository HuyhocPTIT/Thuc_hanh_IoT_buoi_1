"""Bai 1: receive greetings and print topic, payload, and local time."""

from datetime import datetime
import time

from mqtt_common import start_client, stop_client


TOPIC = "iot/lab/message"


def on_connected(client):
    result, _ = client.subscribe(TOPIC, qos=1)
    if result != 0:
        raise ConnectionError(f"Khong subscribe duoc {TOPIC}: {result}")
    print(f"Dang lang nghe {TOPIC}. Nhan Ctrl+C de thoat.")


def on_message(client, userdata, message):
    print("\nNhan duoc message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload.decode('utf-8', errors='replace')}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")


def main():
    client = start_client("bai1-subscriber", on_connected, on_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung subscriber.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
