# Thực hành Python với MQTT — Buổi 1

Ba bài thực hành dùng Python 3 và thư viện `paho-mqtt`. Mỗi bài gồm hai chương trình: bên gửi hoặc thiết bị, và bên nhận hoặc điều khiển. Các chương trình dùng chung cấu hình trong `mqtt_common.py`.

## 1. Chuẩn bị MQTT broker

**Cài thư viện `paho-mqtt` cho client.**
Cài thư viện Python:

```powershell
py -m pip install -r requirements.txt
```

 Tải Mosquitto tại [trang tải chính thức của Eclipse Mosquitto](https://mosquitto.org/download/).

Mở các chương trình từ thư mục chứa các file này. Với mỗi bài, chạy hai lệnh ở **hai terminal khác nhau**. Khởi động chương trình nhận hoặc thiết bị trước.

## 2. Bài 1 — Gửi và nhận thông điệp

Terminal 1:

```powershell
py subscriber_bai1.py
```

Terminal 2:

```powershell
py publisher_bai1.py
```

Publisher hỏi họ tên, mã sinh viên và nội dung thông điệp. Nhấn Enter ở phần nội dung để thoát; có thể gửi nhiều thông điệp liên tiếp. Để gửi một lần không cần nhập tương tác:

```powershell
py publisher_bai1.py --name "Nguyen Quang Huy" --student-id "B23DCCN400" --message "Xin chao tu client Python MQTT"
```

Topic: `iot/lab/message`. Subscriber in topic, payload và thời điểm nhận theo giờ máy đang chạy.

## 3. Bài 2 — Cảm biến nhiệt độ, độ ẩm

Terminal 1:

```powershell
py monitor_subscriber_bai2.py
```

Terminal 2:

```powershell
py sensor_publisher_bai2.py
```

Cảm biến gửi JSON lên `iot/lab/sensor01/data` mỗi 3 giây. Dữ liệu gồm `device_id`, `temperature` và `humidity`. Monitor cảnh báo khi nhiệt độ **> 35 °C** hoặc độ ẩm **< 40%**. Để gửi đúng 5 mẫu rồi thoát, dùng `py sensor_publisher_bai2.py --count 5`.

## 4. Bài 3 — Điều khiển đèn thông minh

Terminal 1:

```powershell
py device_bai3.py
```

Terminal 2:

```powershell
py controller_bai3.py
```

Nhập `ON` hoặc `OFF` để gửi lệnh đến `iot/lab/light01/cmd`; nhập `EXIT` để thoát. Thiết bị phản hồi trạng thái JSON qua `iot/lab/light01/status`, và controller hiển thị trạng thái nhận được. Trạng thái được giữ lại trên broker để controller vừa mở có thể thấy trạng thái gần nhất.

Nhấn `Ctrl+C` để dừng các chương trình chạy liên tục. 
