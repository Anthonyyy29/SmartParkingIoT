# Smart Parking IoT - Backend API

## 📋 Penjelasan Project

Ini adalah backend API untuk sistem **Smart Parking IoT** yang mengelola masuk/keluar kendaraan dan perhitungan biaya parkir.

### Apa yang dilakukan project ini?

- **Catat kendaraan masuk** → Simpan waktu entry ke database
- **Catat kendaraan keluar** → Hitung durasi dan biaya otomatis
- **Lihat kendaraan aktif** → Kendaraan yang sedang parkir
- **Lihat history** → Riwayat kendaraan yang sudah keluar
- **Kelola tarif** → Atur biaya parkir per menit

---

## 📁 Struktur Folder

```
SmartParkingIoT/
├── app/                          # Package utama aplikasi
│   ├── api/                      # Semua endpoints API
│   │   ├── __init__.py
│   │   ├── crud.py              # Logika database (Create, Read, Update)
│   │   └── routes.py            # Definisi semua endpoint API
│   │
│   ├── core/                     # Konfigurasi utama
│   │   ├── __init__.py
│   │   └── config.py            # Database connection & settings
│   │
│   ├── db/                       # Database models
│   │   ├── __init__.py
│   │   └── models.py            # ORM models (ParkingTransaction, Vehicle, ParkingRate)
│   │
│   └── schemas/                  # Validasi request/response (Pydantic)
│       ├── __init__.py
│       └── parking.py           # Schema untuk entry, exit, transaction
│
├── main.py                       # Entry point aplikasi FastAPI
├── requirements.txt              # Dependencies Python
└── README.md                     # Dokumentasi ini
```

---

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Setup Database MySQL

```sql
-- Buat database
CREATE DATABASE smart_parking;

-- Tabel tarif parkir
CREATE TABLE parking_rates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    base_minutes INT NOT NULL,
    base_fee DECIMAL(10,2) NOT NULL,
    per_minute_fee DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert tarif default (60 menit = Rp5000, setelah itu Rp100/menit)
INSERT INTO parking_rates (base_minutes, base_fee, per_minute_fee)
VALUES (60, 5000, 100);
```

### 3. Jalankan Server

```powershell
python main.py
```

atau

```powershell
uvicorn main:app --reload
```

Server akan berjalan di `http://localhost:8000`

---

## 📡 API Endpoints

### Kendaraan Masuk

```
POST /api/entry
Content-Type: application/json

{
  "plate": "B1234ABC",
  "source": "web"
}
```

**Response:**

```json
{
  "status": "ok",
  "transaction_id": 1,
  "entry_time": "2025-11-24T10:30:00"
}
```

---

### Kendaraan Keluar

```
POST /api/exit
Content-Type: application/json

{
  "plate": "B1234ABC",
  "source": "web"
}
```

**Response:**

```json
{
  "status": "ok",
  "plate": "B1234ABC",
  "duration_minutes": 45,
  "fee": 5000,
  "exit_time": "2025-11-24T11:15:00"
}
```

---

### Lihat Kendaraan Aktif (Sedang Parkir)

```
GET /api/active
```

**Response:** List kendaraan dengan status `IN`

---

### Lihat History Kendaraan (Sudah Keluar)

```
GET /api/history
```

**Response:** List kendaraan dengan status `OUT`, `PAID`, atau `DONE`

---

### Lihat Semua Transaksi

```
GET /api/transactions
```

---

### Lihat Semua Kendaraan

```
GET /api/vehicles
```

---

### Lihat Tarif Parkir

```
GET /api/rates
```

---

## 🔧 File-File Penting

| File                     | Fungsi                           |
| ------------------------ | -------------------------------- |
| `app/core/config.py`     | Konfigurasi database MySQL       |
| `app/db/models.py`       | ORM models untuk database        |
| `app/schemas/parking.py` | Validasi request/response        |
| `app/api/crud.py`        | Logika entry, exit, hitung biaya |
| `app/api/routes.py`      | Definisi semua endpoint API      |
| `main.py`                | Aplikasi FastAPI utama           |

---

## 🧮 Cara Perhitungan Biaya

1. **Durasi ≤ 60 menit** → Biaya tetap Rp5.000
2. **Durasi > 60 menit** → Rp5.000 + (menit tambahan × Rp100)

**Contoh:**

- Parkir 30 menit → Rp5.000
- Parkir 90 menit → Rp5.000 + (30 × Rp100) = Rp8.000

---

## 🔐 Security Notes

- Disable CORS (`allow_origins=["*"]`) sebelum production
- Setup environment variables untuk database credentials
- Implementasikan authentication untuk API endpoints

---

## 📚 Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PyMySQL** - MySQL driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

---

## ✅ Keuntungan Struktur Baru

✨ **Lebih Terorganisir** - Folder terpisah per fungsi  
✨ **Mudah di-maintain** - Kode lebih modular  
✨ **Scalable** - Mudah tambah fitur baru  
✨ **Best Practice** - Mengikuti struktur FastAPI yang standard  
✨ **Dokumentasi Jelas** - Setiap file punya tujuan spesifik
