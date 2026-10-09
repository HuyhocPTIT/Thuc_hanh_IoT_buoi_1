"""Bai 2: display sensor readings and warn when thresholds are crossed."""

import json
import time

from mqtt_common import start_client, stop_client


TOPIC = "iot/lab/sensor01/data"


def on_connected(client):
    result, _ = client.subscribe(TOPIC, qos=1)
    if result != 0:
        raise ConnectionError(f"Khong subscribe duoc {TOPIC}: {result}")
    print(f"Dang lang nghe {TOPIC}. Nhan Ctrl+C de thoat.")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        if not isinstance(device_id, str) or not device_id:
            raise ValueError("device_id khong hop le")
        if (isinstance(temperature, bool) or not isinstance(temperature, (int, float))
                or isinstance(humidity, bool) or not isinstance(humidity, (int, float))):
            raise ValueError("temperature/humidity phai la so")
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Bo qua du lieu khong hop le tren {message.topic}: {exc}")
        return

    print(f"\nDevice: {device_id}")
    print(f"Temperature: {temperature} C")
    print(f"Humidity: {humidity} %")
    if temperature > 35:
        print("CANH BAO: Nhiet do cao")
    if humidity < 40:
        print("CANH BAO: Do am thap")


def main():
    client = start_client("bai2-monitor", on_connected, on_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung monitor.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
