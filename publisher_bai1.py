"""Bai 1: publish a greeting with student information."""

import argparse

from mqtt_common import publish_message, start_client, stop_client


TOPIC = "iot/lab/message"


def main():
    parser = argparse.ArgumentParser(description="Gui thong diep MQTT - Bai 1")
    parser.add_argument("--name", help="Ho ten sinh vien")
    parser.add_argument("--student-id", help="Ma sinh vien")
    parser.add_argument("--message", help="Gui mot thong diep roi thoat")
    args = parser.parse_args()

    name = (args.name or input("Ho ten sinh vien: ")).strip()
    student_id = (args.student_id or input("Ma sinh vien: ")).strip()
    if not name or not student_id:
        parser.error("Ho ten va ma sinh vien khong duoc de trong")

    client = start_client("bai1-publisher")
    try:
        print("Nhap noi dung thong diep; Enter de ket thuc.")
        while True:
            message = args.message if args.message is not None else input("Noi dung: ").strip()
            if not message:
                break
            payload = f"{message} - {student_id} - {name}"
            publish_message(client, TOPIC, payload)
            print(f"Da gui [{TOPIC}]: {payload}")
            if args.message is not None:
                break
    except KeyboardInterrupt:
        print("\nDa dung publisher.")
    finally:
        stop_client(client)


if __name__ == "__main__":
    main()
