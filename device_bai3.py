
import json
import time

from mqtt_common import start_client, stop_client


COMMAND_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"
state = "OFF"


def publish_status(client):
    payload = json.dumps({"device_id": "light01", "status": state})
    # Retained status lets a newly started controller see the current light state.
    result = client.publish(STATUS_TOPIC, payload, qos=1, retain=True)
    if result.rc != 0:
        print(f"Khong gui duoc trang thai (ma loi {result.rc})")
    else:
        print(f"Trang thai da gui: {payload}")


def on_connected(client):
    result, _ = client.subscribe(COMMAND_TOPIC, qos=1)
    if result != 0:
        raise ConnectionError(f"Khong subscribe duoc {COMMAND_TOPIC}: {result}")
    print(f"Dang lang nghe lenh tai {COMMAND_TOPIC}. Nhan Ctrl+C de thoat.")
    publish_status(client)


def on_message(client, userdata, message):
    global state
    command = message.payload.decode("utf-8", errors="replace").strip().upper()
    if command not in ("ON", "OFF"):
        print(f"Bo qua lenh khong hop le: {command!r}")
        return
    state = command
    print(f"Da nhan lenh: {command}")
    publish_status(client)


def main():
    client = start_client("bai3-device", on_connected, on_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDa dung thiet bi den.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
