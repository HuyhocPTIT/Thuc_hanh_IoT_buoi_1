"""Shared MQTT connection helpers for the three lab exercises."""

import os
import threading
import uuid

import paho.mqtt.client as mqtt


def start_client(prefix, on_connected=None, on_message=None):
    """Connect, start the network loop, and wait for the broker's response."""
    host = os.getenv("MQTT_HOST", "127.0.0.1")
    port = int(os.getenv("MQTT_PORT", "1883"))
    client_id = f"{prefix}-{uuid.uuid4().hex[:8]}"
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        protocol=mqtt.MQTTv311,
    )

    username = os.getenv("MQTT_USERNAME")
    if username:
        client.username_pw_set(username, os.getenv("MQTT_PASSWORD"))
    if os.getenv("MQTT_TLS", "0").lower() in ("1", "true", "yes"):
        client.tls_set()

    ready = threading.Event()
    connection_error = []

    def handle_connect(connected_client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            connection_error.append(f"Broker tu choi ket noi: {reason_code}")
            ready.set()
            return
        print(f"Da ket noi MQTT broker {host}:{port}")
        try:
            if on_connected is not None:
                on_connected(connected_client)
        except Exception as exc:
            connection_error.append(str(exc))
        finally:
            ready.set()

    def handle_disconnect(connected_client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Mat ket noi MQTT: {reason_code}; dang thu ket noi lai...")

    client.on_connect = handle_connect
    client.on_disconnect = handle_disconnect
    client.on_message = on_message

    try:
        client.connect(host, port, keepalive=60)
        client.loop_start()
        if not ready.wait(10):
            raise TimeoutError("Khong nhan duoc phan hoi tu MQTT broker sau 10 giay")
        if connection_error:
            raise ConnectionError(connection_error[0])
    except OSError as exc:
        client.disconnect()
        client.loop_stop()
        raise SystemExit(
            f"Khong ket noi duoc MQTT broker tai {host}:{port} ({exc}). "
            "Hay khoi dong broker, hoac kiem tra MQTT_HOST va MQTT_PORT."
        ) from None
    except Exception:
        client.disconnect()
        client.loop_stop()
        raise
    return client


def publish_message(client, topic, payload, retain=False):
    """Publish and confirm that Paho handed the message to the broker."""
    info = client.publish(topic, payload, qos=1, retain=retain)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        raise ConnectionError(f"Khong gui duoc MQTT message (ma loi {info.rc})")
    info.wait_for_publish(timeout=10)
    if not info.is_published():
        raise TimeoutError("Qua thoi gian cho broker xac nhan message")


def stop_client(client):
    client.disconnect()
    client.loop_stop()
