THUC HANH PYTHON MQTT - BUOI 1

Broker: Mosquitto (hoac broker MQTT tuong thich) tai 127.0.0.1:1883 theo mac dinh.
Neu chua co broker, tai Mosquitto tu https://mosquitto.org/download/ va khoi dong:
  & "C:\Program Files\mosquitto\mosquitto.exe" -v
Kiem tra: Test-NetConnection 127.0.0.1 -Port 1883
Chi chay code khi TcpTestSucceeded la True.
Neu dung broker khac, dat MQTT_HOST va MQTT_PORT trong moi terminal.
Neu broker can tai khoan, dat MQTT_USERNAME, MQTT_PASSWORD; neu can TLS, dat MQTT_TLS=1.

Can Python 3 va paho-mqtt 2.x. Cai bang: py -m pip install -r requirements.txt
Mo hai terminal trong thu muc nay, chay chuong trinh nhan/thiet bi truoc:

Bai 1: py subscriber_bai1.py  |  py publisher_bai1.py
       Publisher hoi ho ten, ma sinh vien va noi dung. Enter o noi dung de thoat.
       Ket qua: subscriber in topic, payload, thoi diem nhan.

Bai 2: py monitor_subscriber_bai2.py  |  py sensor_publisher_bai2.py
       Cam bien gui JSON moi 3 giay. Monitor hien thi nhiet do, do am va canh bao
       khi nhiet do > 35 C hoac do am < 40%.

Bai 3: py device_bai3.py  |  py controller_bai3.py
       Nhap ON/OFF tai controller, EXIT de thoat. Device gui trang thai JSON;
       controller hien thi trang thai nhan duoc.

Nhan Ctrl+C de dung cac chuong trinh chay lien tuc.
Xem README.md de biet cau hinh va cach chay chi tiet.
