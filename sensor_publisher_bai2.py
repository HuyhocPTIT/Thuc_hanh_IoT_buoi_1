"""Bai 2: simulate a temperature/humidity sensor every three seconds."""

import argparse
import json
import random
import time

from mqtt_common import publish_message, start_client, stop_client


TOPIC = "iot/lab/sensor01/data"


def main():
    parser = argparse.ArgumentParser(description="Mo phong cam bien MQTT - Bai 2")
    parser.add_argument("--count", type=int, help="So lan gui; mac dinh gui lien tuc")
    args = parser.parse_args()
    if args.count is not None and args.count < 1:
        parser.error("--count phai lon hon 0")

    client = start_client("bai2-sensor")
    try:
        sent = 0
        while args.count is None or sent < args.count:
            data = {
                "device_id": "sensor01",
                "temperature": round(random.uniform(20.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
            }
            payload = json.dumps(data)
            publish_message(client, TOPIC, payload)
            print(f"Da gui [{TOPIC}]: {payload}")
            sent += 1
            if args.count is None or sent < args.count:
                time.sleep(3)
    except KeyboardInterrupt:
        print("\nDa dung cam bien.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
