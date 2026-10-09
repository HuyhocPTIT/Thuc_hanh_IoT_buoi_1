
import json

from mqtt_common import publish_message, start_client, stop_client


COMMAND_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"


def on_connected(client):
    result, _ = client.subscribe(STATUS_TOPIC, qos=1)
    if result != 0:
        raise ConnectionError(f"Khong subscribe duoc {STATUS_TOPIC}: {result}")
    print(f"Dang lang nghe trang thai tai {STATUS_TOPIC}.")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        if data.get("device_id") != "light01" or data.get("status") not in ("ON", "OFF"):
            raise ValueError("payload trang thai khong hop le")
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, ValueError) as exc:
        print(f"Bo qua trang thai khong hop le: {exc}")
        return
    print(f"\nTrang thai nhan duoc: {json.dumps(data, ensure_ascii=False)}")


def main():
    client = start_client("bai3-controller", on_connected, on_message)
    try:
        while True:
            command = input("Nhap lenh (ON/OFF/EXIT): ").strip().upper()
            if command == "EXIT":
                break
            if command not in ("ON", "OFF"):
                print("Lenh khong hop le. Chi nhap ON, OFF hoac EXIT.")
                continue
            publish_message(client, COMMAND_TOPIC, command)
            print(f"Da gui lenh {command} toi light01")
    except KeyboardInterrupt:
        print("\nDa dung controller.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
