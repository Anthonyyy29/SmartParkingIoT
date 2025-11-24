# 📚 API REFERENCE - SMART PARKING IOT BACKEND

Dokumentasi lengkap REST API untuk Smart Parking IoT Backend.

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Format:** JSON

---

## 🎯 OVERVIEW

Smart Parking IoT Backend adalah REST API untuk sistem parkir IoT yang mengelola:

- Entry kendaraan (masuk parkir)
- Exit kendaraan (keluar parkir)
- Perhitungan otomatis biaya parkir
- Monitoring real-time status parkir

**Fitur Utama:**

- ✅ Entry/Exit tracking berbasis UID (RFID)
- ✅ Perhitungan otomatis biaya parkir real-time
- ✅ Deteksi duplikat (cegah entry ganda)
- ✅ API monitoring untuk admin dashboard
- ✅ Dokumentasi interaktif (Swagger UI)

---

## 📊 PRICING FORMULA

**Formula Perhitungan Biaya:**

```
Biaya = 5000 + (ceil(durasi_menit/60) - 1) × 2000
```

**Breakdown:**

- **Jam Pertama (60 menit):** Rp 5.000
- **Setiap Jam Tambahan:** Rp 2.000

**Contoh:**

- 45 menit → Rp 5.000 (< 1 jam)
- 75 menit → Rp 7.000 (1 jam + 15 menit = 2 jam)
- 150 menit → Rp 9.000 (2 jam + 30 menit = 3 jam)
- 305 menit → Rp 13.000 (5 jam + 5 menit = 6 jam)

---

## 🔌 ENDPOINTS

### 1. Health Check

**Cek status API dan database connection**

```http
GET /health
```

**Response (200):**

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-24T14:30:00"
}
```

---

### 2. Entry - Kendaraan Masuk Parkir

**Mencatat kendaraan masuk parkir**

```http
POST /api/entry
Content-Type: application/json
```

**Request Body:**

```json
{
  "uid": "RFID_001"
}
```

**Field Requirements:**

- `uid` (string, required)
  - Format: alphanumeric, max 50 karakter
  - Contoh: `"CAR001"`, `"RFID_ABC123"`, `"E004BE1234"`

**Response (200) - Success:**

```json
{
  "success": true,
  "message": "Vehicle entry recorded successfully",
  "transaction_id": 5,
  "uid": "RFID_001",
  "entry_time": "2025-11-24T14:30:00.000000",
  "vehicle_status": "IN"
}
```

**Response (400) - Duplicate Entry:**

```json
{
  "success": false,
  "error_code": "ALREADY_PARKED",
  "message": "Vehicle RFID_001 is already parked",
  "vehicle_status": "IN"
}
```

**Response (400) - Invalid UID:**

```json
{
  "success": false,
  "error_code": "INVALID_UID",
  "message": "UID cannot be empty or exceed 50 characters"
}
```

**Response (500) - Database Error:**

```json
{
  "success": false,
  "error_code": "DATABASE_ERROR",
  "message": "Failed to record vehicle entry: [detail error]"
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid":"RFID_001"}'
```

**Python Example:**

```python
import requests

url = "http://localhost:8000/api/entry"
payload = {"uid": "RFID_001"}
response = requests.post(url, json=payload)
print(response.json())
```

---

### 3. Exit - Kendaraan Keluar Parkir

**Mencatat kendaraan keluar dan menghitung biaya parkir**

```http
POST /api/exit
Content-Type: application/json
```

**Request Body:**

```json
{
  "uid": "RFID_001"
}
```

**Field Requirements:**

- `uid` (string, required)
  - Format: alphanumeric, max 50 karakter
  - Harus match dengan UID saat entry

**Response (200) - Success:**

```json
{
  "success": true,
  "message": "Vehicle exit recorded successfully",
  "uid": "RFID_001",
  "transaction_id": 5,
  "entry_time": "2025-11-24T14:30:00.000000",
  "exit_time": "2025-11-24T14:45:00.000000",
  "duration_minutes": 15,
  "fee": 5000,
  "fee_formatted": "Rp 5.000",
  "vehicle_status": "OUT"
}
```

**Response (400) - Not Found:**

```json
{
  "success": false,
  "error_code": "NOT_FOUND",
  "message": "No active parking session found for vehicle RFID_001"
}
```

**Response (400) - Invalid UID:**

```json
{
  "success": false,
  "error_code": "INVALID_UID",
  "message": "UID cannot be empty or exceed 50 characters"
}
```

**Response (500) - Database Error:**

```json
{
  "success": false,
  "error_code": "DATABASE_ERROR",
  "message": "Failed to record vehicle exit: [detail error]"
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid":"RFID_001"}'
```

**Python Example:**

```python
import requests

url = "http://localhost:8000/api/exit"
payload = {"uid": "RFID_001"}
response = requests.post(url, json=payload)
data = response.json()
print(f"Durasi: {data['duration_minutes']} menit")
print(f"Biaya: {data['fee_formatted']}")
```

---

### 4. Parking Status - Status Parkir Real-time

**Mendapat semua kendaraan yang sedang parkir dengan info real-time**

```http
GET /api/parking-status
```

**Query Parameters:** None

**Response (200):**

```json
{
  "success": true,
  "timestamp": "2025-11-24T14:35:00",
  "total_vehicles_parked": 2,
  "vehicles": [
    {
      "uid": "RFID_001",
      "entry_time": "2025-11-24T14:30:00.000000",
      "duration_minutes": 5,
      "current_fee": 5000,
      "current_fee_formatted": "Rp 5.000"
    },
    {
      "uid": "RFID_002",
      "entry_time": "2025-11-24T13:45:00.000000",
      "duration_minutes": 50,
      "current_fee": 5000,
      "current_fee_formatted": "Rp 5.000"
    }
  ]
}
```

**Field Details:**

- `duration_minutes`: Durasi parkir hingga sekarang (real-time)
- `current_fee`: Biaya yang harus dibayar jika keluar sekarang
- Biaya dihitung real-time, bukan stored di database

**cURL Example:**

```bash
curl http://localhost:8000/api/parking-status
```

**Python Example:**

```python
import requests

url = "http://localhost:8000/api/parking-status"
response = requests.get(url)
data = response.json()

print(f"Total kendaraan parkir: {data['total_vehicles_parked']}")
for vehicle in data['vehicles']:
    print(f"UID: {vehicle['uid']}, Durasi: {vehicle['duration_minutes']} menit")
```

---

### 5. Last Transaction - Transaksi Terakhir Kendaraan

**Mendapat transaksi terakhir (bisa entry atau exit) dari kendaraan**

```http
GET /api/last-transaction/{uid}
```

**Path Parameters:**

- `uid` (string, required): UID kendaraan

**Response (200) - Vehicle Currently Parked:**

```json
{
  "success": true,
  "uid": "RFID_001",
  "transaction_id": 5,
  "status": "IN",
  "entry_time": "2025-11-24T14:30:00.000000",
  "exit_time": null,
  "duration_minutes": null,
  "fee": null,
  "message": "Vehicle is currently parked"
}
```

**Response (200) - Vehicle Already Exited:**

```json
{
  "success": true,
  "uid": "RFID_001",
  "transaction_id": 4,
  "status": "OUT",
  "entry_time": "2025-11-24T14:00:00.000000",
  "exit_time": "2025-11-24T14:25:00.000000",
  "duration_minutes": 25,
  "fee": 5000,
  "fee_formatted": "Rp 5.000",
  "message": "Vehicle successfully exited"
}
```

**Response (404) - Not Found:**

```json
{
  "success": false,
  "error_code": "NOT_FOUND",
  "message": "No transaction history found for vehicle RFID_999"
}
```

**cURL Example:**

```bash
curl http://localhost:8000/api/last-transaction/RFID_001
```

**Python Example:**

```python
import requests

uid = "RFID_001"
url = f"http://localhost:8000/api/last-transaction/{uid}"
response = requests.get(url)
data = response.json()

if data['success']:
    print(f"Status: {data['status']}")
    if data['status'] == 'OUT':
        print(f"Biaya: {data['fee_formatted']}")
    else:
        print("Kendaraan masih parkir")
```

---

## 🚀 QUICK START EXAMPLES

### Skenario 1: Kendaraan Masuk Parkir

```bash
# Step 1: Kendaraan masuk
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid":"CAR001"}'

# Response:
# {
#   "success": true,
#   "transaction_id": 1,
#   "entry_time": "2025-11-24T14:30:00"
# }
```

### Skenario 2: Cek Status Parkir

```bash
# Step 1: Lihat semua kendaraan parkir
curl http://localhost:8000/api/parking-status

# Response:
# {
#   "total_vehicles_parked": 1,
#   "vehicles": [
#     {
#       "uid": "CAR001",
#       "duration_minutes": 15,
#       "current_fee": 5000
#     }
#   ]
# }
```

### Skenario 3: Kendaraan Keluar Parkir

```bash
# Step 1: Kendaraan keluar (setelah 15 menit)
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid":"CAR001"}'

# Response:
# {
#   "success": true,
#   "duration_minutes": 15,
#   "fee": 5000,
#   "vehicle_status": "OUT"
# }
```

---

## ⚙️ ERROR CODES

Daftar lengkap error codes yang mungkin dikembalikan:

| Error Code       | Status | Penjelasan                           |
| ---------------- | ------ | ------------------------------------ |
| `INVALID_UID`    | 400    | UID kosong atau > 50 karakter        |
| `ALREADY_PARKED` | 400    | Kendaraan sudah parkir (entry ganda) |
| `NOT_FOUND`      | 404    | Transaksi/kendaraan tidak ditemukan  |
| `DATABASE_ERROR` | 500    | Kesalahan database                   |
| `INTERNAL_ERROR` | 500    | Error internal server                |

---

## 📱 INTEGRATION EXAMPLES

### Python IoT Client

```python
import requests

class SmartParkingClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def record_entry(self, uid):
        response = requests.post(
            f"{self.base_url}/api/entry",
            json={"uid": uid}
        )
        return response.json()

    def record_exit(self, uid):
        response = requests.post(
            f"{self.base_url}/api/exit",
            json={"uid": uid}
        )
        return response.json()

    def get_parking_status(self):
        response = requests.get(f"{self.base_url}/api/parking-status")
        return response.json()

# Usage
client = SmartParkingClient("http://localhost:8000")

# Kendaraan masuk
entry_response = client.record_entry("RFID_001")
print(f"Entry berhasil: {entry_response['success']}")

# Cek status
status = client.get_parking_status()
print(f"Total parkir: {status['total_vehicles_parked']}")

# Kendaraan keluar
exit_response = client.record_exit("RFID_001")
print(f"Biaya parkir: Rp {exit_response['fee']}")
```

### JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000";

async function recordEntry(uid) {
  const response = await fetch(`${BASE_URL}/api/entry`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ uid }),
  });
  return response.json();
}

async function recordExit(uid) {
  const response = await fetch(`${BASE_URL}/api/exit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ uid }),
  });
  return response.json();
}

async function getParkingStatus() {
  const response = await fetch(`${BASE_URL}/api/parking-status`);
  return response.json();
}

// Usage
(async () => {
  const entry = await recordEntry("RFID_001");
  console.log("Entry berhasil:", entry.success);

  const status = await getParkingStatus();
  console.log("Total parkir:", status.total_vehicles_parked);
})();
```

---

## 🔐 CORS Configuration

API sudah dikonfigurasi CORS untuk development. Allowed origins:

- `http://localhost:3000`
- `http://localhost:8080`
- `http://localhost`
- Semua localhost origins

Untuk production, ubah di `main.py`:

```python
allow_origins=[
    "https://yourdomain.com",
    "https://admin.yourdomain.com"
]
```

---

## 📊 RESPONSE FORMAT

Semua response mengikuti format standar:

**Success Response:**

```json
{
  "success": true,
  "message": "Deskripsi operasi berhasil",
  "data": {
    /* data operasi */
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error_code": "ERROR_CODE",
  "message": "Deskripsi error"
}
```

---

## 🧪 TESTING DENGAN SWAGGER UI

Dokumentasi interaktif tersedia di:

```
http://localhost:8000/docs
```

Features:

- ✅ Dokumentasi otomatis semua endpoints
- ✅ Request/Response examples
- ✅ Try it out - test endpoint langsung di browser
- ✅ Schema validation

---

## 🚀 DEPLOYMENT

### Local Development

```bash
python main.py
```

### Production (Railway/Render)

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

Lihat file `.env.example` untuk konfigurasi production.

---

## 📞 SUPPORT

- Documentasi: Lihat file `SETUP_GUIDE_ID.md` untuk setup
- Contoh IoT: Lihat file `iot_client_example.py`
- Troubleshooting: Lihat file `QUICK_REFERENCE_ID.md`

---

**Happy Integration! 🚀**
