# Thực hành Python với MQTT — Buổi 1

Ba bài thực hành dùng Python 3 và thư viện `paho-mqtt` 2.x. Mỗi bài gồm hai chương trình: bên gửi hoặc thiết bị, và bên nhận hoặc điều khiển. Các chương trình dùng chung cấu hình trong `mqtt_common.py`.

## 1. Chuẩn bị MQTT broker

Bạn cần một broker MQTT có thể truy cập được, chẳng hạn Mosquitto chạy trên máy. **Cài `paho-mqtt` chỉ cài thư viện cho client Python; nó không khởi động broker.** Trên Windows, nếu chưa có Mosquitto, tải bộ cài tại [trang tải chính thức của Eclipse Mosquitto](https://mosquitto.org/download/). Sau khi cài, mở một PowerShell riêng và chạy broker (điều chỉnh đường dẫn nếu bạn cài ở nơi khác):

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -v
```

Giữ cửa sổ broker mở trong lúc thực hành. Nếu Mosquitto đã chạy dưới dạng Windows service, không cần mở thêm tiến trình. Kiểm tra broker có nhận kết nối ở cổng mặc định hay chưa:

```powershell
Test-NetConnection 127.0.0.1 -Port 1883
```

Chỉ chạy các chương trình Python khi `TcpTestSucceeded` là `True`. Mosquitto chạy không kèm file cấu hình mặc định lắng nghe trên máy cục bộ ở cổng `1883`. Cài thư viện Python:

```powershell
py -m pip install -r requirements.txt
```

Mặc định chương trình kết nối tới `127.0.0.1:1883` và không dùng tài khoản hoặc TLS. Nếu broker ở nơi khác, thiết lập biến môi trường trong **mỗi cửa sổ terminal** trước khi chạy chương trình:

```powershell
$env:MQTT_HOST = "dia-chi-broker"
$env:MQTT_PORT = "1883"
```

Nếu broker yêu cầu tài khoản, thêm `$env:MQTT_USERNAME = "ten-dang-nhap"` và `$env:MQTT_PASSWORD = "mat-khau"`. Nếu broker yêu cầu TLS, đặt `$env:MQTT_TLS = "1"` và dùng đúng cổng TLS của broker, thường là `8883`. Chương trình xác minh chứng chỉ theo cấu hình mặc định của hệ điều hành.

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
py publisher_bai1.py --name "Nguyen Van A" --student-id "B23DCCN001" --message "Xin chao tu client Python MQTT"
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

Nhấn `Ctrl+C` để dừng các chương trình chạy liên tục. Nếu kết nối thất bại, kiểm tra broker đang chạy, địa chỉ/cổng, tài khoản và TLS ở cả hai terminal.
