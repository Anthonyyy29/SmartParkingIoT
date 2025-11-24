# Smart Parking IoT - Backend API

FastAPI web server untuk sistem smart parking IoT yang deployable.

## 📋 Overview

Sistem parking management yang terintegrasi dengan IoT devices untuk:

- ✅ Mencatat waktu masuk kendaraan via RFID gate
- ✅ Mencatat waktu keluar dan menghitung biaya parkir
- ✅ Monitoring real-time kendaraan yang sedang parkir
- ✅ Admin dashboard untuk reporting

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Database**: MySQL (via XAMPP)
- **Driver**: mysql-connector-python
- **Server**: Uvicorn

## 📦 Prerequisites

- Python 3.12.1
- XAMPP (MySQL)
- pip (Python package manager)

## 🚀 Quick Start

### 1. Setup Database

#### Di XAMPP phpMyAdmin:

1. Buka `http://localhost/phpmyadmin/`
2. Create database baru: **`smart_parking_db`**
3. Import file: `database/schema.sql`

Atau via command line:

```bash
mysql -u root < database/schema.sql
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy dari template:

```bash
cp .env.example .env
```

Edit `.env` sesuai konfigurasi lokal:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=smart_parking_db
API_PORT=8000
DEBUG=True
```

### 4. Run Server

```bash
python main.py
```

Server akan berjalan di `http://localhost:8000`

### Akses API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### Health Check

#### GET /

Check API status

```bash
curl http://localhost:8000/
```

#### GET /health

Check API & database health

```bash
curl http://localhost:8000/health
```

---

### Vehicle Entry

#### POST /api/entry

Record kendaraan masuk parking

**Request:**

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid": "1A2B3C4D"}'
```

**Request Body:**

```json
{
  "uid": "1A2B3C4D"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "Vehicle entry recorded successfully",
  "transaction_id": 1,
  "entry_time": "2025-11-24T14:30:00"
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "Vehicle is already in parking",
  "code": "ALREADY_PARKED"
}
```

**Error Codes:**

- `INVALID_UID` - UID format tidak valid
- `INVALID_UID_FORMAT` - UID terlalu panjang
- `ALREADY_PARKED` - Kendaraan sudah parkir (status IN)
- `DATABASE_ERROR` - Error database

---

### Vehicle Exit

#### POST /api/exit

Record kendaraan keluar parking dan hitung biaya

**Request:**

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid": "1A2B3C4D"}'
```

**Request Body:**

```json
{
  "uid": "1A2B3C4D"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "Vehicle exit recorded successfully",
  "transaction_id": 1,
  "uid": "1A2B3C4D",
  "entry_time": "2025-11-24T14:30:00",
  "exit_time": "2025-11-24T15:45:00",
  "duration_minutes": 75,
  "fee": 7000.0,
  "status": "OUT"
}
```

**Error Response (404):**

```json
{
  "success": false,
  "error": "Vehicle not found in parking",
  "code": "NOT_FOUND"
}
```

**Error Codes:**

- `INVALID_UID` - UID format tidak valid
- `NOT_FOUND` - Kendaraan tidak ditemukan atau sudah keluar
- `DATABASE_ERROR` - Error database

---

### Parking Status (Admin)

#### GET /api/parking-status

Dapatkan list kendaraan yang sedang parkir

**Request:**

```bash
curl http://localhost:8000/api/parking-status
```

**Success Response (200):**

```json
{
  "success": true,
  "active_vehicles": 2,
  "vehicles": [
    {
      "uid": "1A2B3C4D",
      "entry_time": "2025-11-24T14:30:00",
      "duration_minutes": 45,
      "fee": 5000.0
    },
    {
      "uid": "5E6F7G8H",
      "entry_time": "2025-11-24T13:15:00",
      "duration_minutes": 90,
      "fee": 7000.0
    }
  ]
}
```

---

### Last Transaction

#### GET /api/last-transaction/{uid}

Dapatkan transaksi terakhir kendaraan tertentu

**Request:**

```bash
curl http://localhost:8000/api/last-transaction/1A2B3C4D
```

**Success Response (200):**

```json
{
  "success": true,
  "uid": "1A2B3C4D",
  "entry_time": "2025-11-24T14:30:00",
  "exit_time": "2025-11-24T15:45:00",
  "duration_minutes": 75,
  "fee": 7000.0,
  "status": "OUT"
}
```

**Not Found Response (404):**

```json
{
  "success": false,
  "error": "No transaction found for this vehicle",
  "code": "NOT_FOUND"
}
```

---

## 💰 Pricing Structure

| Duration                   | Fee      |
| -------------------------- | -------- |
| 0 - 60 menit               | Rp 5.000 |
| 61 - 120 menit             | Rp 7.000 |
| 121 - 180 menit            | Rp 9.000 |
| dst (setiap jam +Rp 2.000) |          |

**Rumus Kalkulasi:**

```
fee = 5000 + (ceil(duration_minutes / 60) - 1) * 2000
```

**Contoh:**

- 45 menit → Rp 5.000
- 60 menit → Rp 5.000
- 75 menit → Rp 7.000
- 120 menit → Rp 7.000
- 150 menit → Rp 9.000

---

## 🔗 Integrasi IoT Device

### Gerbang Masuk (Entry Gate)

```python
import requests
import time

API_URL = "http://localhost:8000/api/entry"

# Baca UID dari sensor RFID
uid = "1A2B3C4D"

# Kirim ke server
response = requests.post(API_URL, json={"uid": uid})
data = response.json()

if data["success"]:
    print(f"✅ Masuk tercatat - ID: {data['transaction_id']}")
    # Buka gerbang
else:
    print(f"❌ Error: {data['error']}")
    # Tampilkan error di LCD/display
```

### Gerbang Keluar (Exit Gate)

```python
import requests

API_URL = "http://localhost:8000/api/exit"

# Baca UID dari sensor RFID
uid = "1A2B3C4D"

# Kirim ke server
response = requests.post(API_URL, json={"uid": uid})
data = response.json()

if data["success"]:
    fee = data["fee"]
    duration = data["duration_minutes"]
    print(f"✅ Biaya parkir: Rp {fee:,.0f}")
    print(f"   Durasi: {duration} menit")
    # Buka gerbang + tampilkan biaya di display
else:
    print(f"❌ Error: {data['error']}")
    # Tampilkan error di LCD/display
```

---

## 📊 Admin Dashboard

Web admin client untuk monitoring real-time kendaraan yang parkir.

### Setup

Lihat: `web_admin/README.md`

### Features

- ✅ Real-time monitoring kendaraan parkir
- ✅ Total revenue harian
- ✅ Auto-refresh setiap 5 detik
- ✅ Responsive design
- ✅ Pricing information

### Akses

- **Option 1 (Recommended)**: `http://localhost/parking_admin/` (dari XAMPP)
- **Option 2**: Buka `web_admin/index.html` langsung

---

## ☁️ Cloud Deployment

### Preparation

1. **Environment Variables**

   - Update `.env` dengan cloud database credentials
   - Set `DEBUG=False` untuk production

2. **Create Procfile** (untuk Heroku/Railway)

   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Docker Support** (Optional)
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

### Deploy to Railway

1. Push ke GitHub
2. Login ke Railway.app
3. New Project → Import GitHub repo
4. Connect database (Railway MySQL)
5. Deploy!

Dokumentasi lengkap: [Railway Docs](https://docs.railway.app)

---

## 📁 Project Structure

```
SmartParkingIoT/
├── main.py                      # FastAPI entry point
├── config.py                    # Configuration management
├── database_connection.py       # MySQL connection pool
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── database/
│   └── schema.sql              # Database schema (import ini)
├── models/
│   └── schemas.py              # Pydantic models
├── utils/
│   └── pricing.py              # Pricing calculation
├── routes/
│   ├── entry.py                # /api/entry endpoint
│   ├── exit.py                 # /api/exit endpoint
│   └── admin.py                # /api/parking-status endpoint
└── web_admin/                  # Admin dashboard (copy ke htdocs)
    ├── index.html
    ├── style.css
    ├── script.js
    └── README.md
```

---

## 🐛 Troubleshooting

### Database Connection Error

```
❌ Connection error: Unknown database 'smart_parking_db'
```

**Solution:**

```bash
# Buat database
mysql -u root -e "CREATE DATABASE smart_parking_db;"
# Import schema
mysql -u root smart_parking_db < database/schema.sql
```

### Port Already in Use

```
OSError: [Errno 10048] Only one usage of each socket address
```

**Solution:**

```bash
# Change port di .env
API_PORT=8001
```

Atau kill process:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### CORS Error di Admin Dashboard

```
Access to XMLHttpRequest blocked by CORS
```

**Solution:**

- Update `API_BASE_URL` di `web_admin/script.js`
- Atau check CORS configuration di `main.py`

---

## 📝 Logs & Debugging

Enable debug mode di `.env`:

```env
DEBUG=True
```

Run dengan verbose logging:

```bash
python main.py --log-level debug
```

---

## 📞 Support

Untuk pertanyaan atau issue, silakan contact developer atau buka issue di GitHub.

---

## 📄 License

Project ini milik Politeknik Negeri Jakarta (Smart Parking IoT System)

**Last Updated**: November 24, 2025
**Version**: 1.0.0
