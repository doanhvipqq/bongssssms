# SMS API Service

RESTful API Service để gửi SMS OTP qua nhiều dịch vụ Việt Nam sử dụng FastAPI.

## 📋 Tính Năng

- ✅ **1800+ SMS Services**: Tích hợp hơn 1800 functions từ các dịch vụ khác nhau
- ✅ **Auto Load Balancing**: Tự động chọn ngẫu nhiên các dịch vụ để gửi SMS
- ✅ **Concurrent Execution**: Gửi SMS song song qua nhiều dịch vụ cùng lúc
- ✅ **RESTful API**: Endpoints chuẩn REST với Swagger UI documentation
- ✅ **Error Handling**: Xử lý lỗi toàn diện, retry mechanism
- ✅ **CORS Support**: Cho phép truy cập từ mọi origin

## 🚀 Cài Đặt

### 1. Install Dependencies

```bash
cd C:\Users\Administrator\Downloads\api_sms
pip install -r requirements.txt
```

### 2. Start Server

```bash
python main.py
```

Hoặc sử dụng uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: `http://localhost:8000`

## 📚 API Endpoints

### 1. Get API Info
```
GET /
```

### 2. Health Check
```
GET /health
```

### 3. List Available Services
```
GET /api/sms/services
```

Response:
```json
{
  "status": "success",
  "total": 1800,
  "services": ["momo", "viettel", "vieon", "tiki", "fpt", ...]
}
```

### 4. Send SMS Batch (Auto Spam)
```
POST /api/sms/send
Content-Type: application/json

{
  "phone": "0123456789",
  "amount": 10
}
```

Response:
```json
{
  "status": "completed",
  "message": "Đã gửi SMS qua 8/10 dịch vụ",
  "data": {
    "phone": "0123456789",
    "requested": 10,
    "total_services": 10,
    "success_count": 8,
    "error_count": 2,
    "results": [...]
  }
}
```

### 5. Send SMS Single Service
```
POST /api/sms/single
Content-Type: application/json

{
  "phone": "0123456789",
  "service_name": "momo"
}
```

## 🌐 Swagger UI

Mở browser và truy cập: `http://localhost:8000/docs`

Tại đây bạn có thể:
- Xem tất cả endpoints
- Test API trực tiếp
- Xem request/response models

## 📝 Usage Examples

### Using cURL

```bash
# Send SMS via 5 random services
curl -X POST http://localhost:8000/api/sms/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "0123456789", "amount": 5}'

# Send SMS via specific service
curl -X POST http://localhost:8000/api/sms/single \
  -H "Content-Type: application/json" \
  -d '{"phone": "0123456789", "service_name": "momo"}'

# List all services
curl http://localhost:8000/api/sms/services
```

### Using Python

```python
import requests

# Send batch SMS
response = requests.post(
    "http://localhost:8000/api/sms/send",
    json={"phone": "0123456789", "amount": 10}
)
print(response.json())

# Send single SMS
response = requests.post(
    "http://localhost:8000/api/sms/single",
    json={"phone": "0123456789", "service_name": "viettel"}
)
print(response.json())
```

### Using JavaScript

```javascript
// Send batch SMS
fetch('http://localhost:8000/api/sms/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone: '0123456789',
    amount: 10
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## ⚙️ Configuration

Chỉnh sửa file `config.py` để thay đổi cấu hình:

- `API_HOST`: Host address (default: "0.0.0.0")
- `API_PORT`: Port number (default: 8000)
- `MAX_WORKERS`: Số thread pool (default: 10)
- `REQUEST_TIMEOUT`: Timeout cho mỗi request (default: 30s)

## 🔧 Troubleshooting

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Port already in use
Thay đổi port trong `config.py` hoặc chạy:
```bash
uvicorn main:app --port 8001
```

### Lỗi: Services not loading
Kiểm tra thư mục `services/` có đầy đủ 5 files:
- smsvip_0.py
- smsvip_1.py
- smsvip_2.py
- smsvip_3.py
- smsvip_4.py

## 📦 Project Structure

```
api_sms/
├── main.py              # FastAPI application
├── smsvip_loader.py     # Service loader module
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── services/            # SMS service files
│   ├── smsvip_0.py
│   ├── smsvip_1.py
│   ├── smsvip_2.py
│   ├── smsvip_3.py
│   └── smsvip_4.py
└── README.md            # This file
```

## 🎯 Common Services

Một số dịch vụ phổ biến có sẵn:
- `momo` - MoMo wallet
- `viettel` - Viettel
- `vieon` - VieON
- `tiki` - Tiki
- `fpt` - FPT
- `gotadi` - Gotadi
- `tv360` - TV360
- `winmart` - Winmart
- `ahamove` - Ahamove
- ... và 1800+ services khác

## 📄 License

Free to use

## 👨‍💻 Author

Created by Bóng X - Trần Đức Doanh
