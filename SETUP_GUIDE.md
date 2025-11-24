# 🚀 SETUP GUIDE - Smart Parking IoT Backend

Panduan lengkap setup dan cara menggunakan Smart Parking IoT Backend API.

---

## ✅ CHECKLIST SEBELUM MULAI

- [x] Python 3.12.1 terinstall
- [x] XAMPP (MySQL) running
- [x] File ini sudah dibaca dan dipahami

---

## 📝 STEP-BY-STEP SETUP

### STEP 1️⃣: Buat Database di XAMPP

1. **Buka XAMPP Control Panel**

   - Start Apache dan MySQL

2. **Buka phpMyAdmin**

   - Buka browser: `http://localhost/phpmyadmin/`
   - Login (default: user=root, password=kosong)

3. **Buat Database Baru**

   - Di sidebar kiri, klik **"New"**
   - Nama database: **`smart_parking_db`**
   - Charset: `utf8mb4_general_ci`
   - Klik **Create**

4. **Import Schema SQL**

   - Pilih database `smart_parking_db` yang baru dibuat
   - Tab **Import**
   - Choose file: `database/schema.sql` (ada di folder project)
   - Klik **Import**

   ✅ Database sekarang punya 3 tabel: `vehicles`, `parking_rates`, `parking_transactions`

**Alternative (Via Command Line):**

```bash
# Di folder SmartParkingIoT
mysql -u root smart_parking_db < database/schema.sql
```

---

### STEP 2️⃣: Install Python Dependencies

```bash
# Navigate ke folder project
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"

# Install semua package
pip install -r requirements.txt
```

✅ Selesai! Semua library sudah terinstall.

---

### STEP 3️⃣: Verifikasi .env Configuration

File `.env` sudah dibuat otomatis. Check apakah benar:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=smart_parking_db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

**Note:**

- Jika MySQL password Anda bukan kosong, ubah `DB_PASSWORD`
- Jika port MySQL bukan 3306, ubah `DB_PORT`

---

### STEP 4️⃣: Jalankan FastAPI Server

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
python main.py
```

**Expected Output:**

```
🚀 Starting Smart Parking IoT API...
✅ Connected to smart_parking_db database
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ Server berjalan! Akses di `http://localhost:8000`

---

## 🧪 TEST API

### Test 1: Health Check

**Via Browser atau cURL:**

```bash
curl http://localhost:8000/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-24T14:30:00.123456"
}
```

---

### Test 2: Vehicle Entry

**Via Postman atau cURL:**

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid": "1A2B3C4D"}'
```

**Expected Response (Success):**

```json
{
  "success": true,
  "message": "Vehicle entry recorded successfully",
  "transaction_id": 1,
  "entry_time": "2025-11-24T14:30:00"
}
```

---

### Test 3: Vehicle Exit

**Via cURL (setelah tunggu beberapa detik):**

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid": "1A2B3C4D"}'
```

**Expected Response (Success):**

```json
{
  "success": true,
  "message": "Vehicle exit recorded successfully",
  "transaction_id": 1,
  "uid": "1A2B3C4D",
  "entry_time": "2025-11-24T14:30:00",
  "exit_time": "2025-11-24T14:35:00",
  "duration_minutes": 5,
  "fee": 5000.0,
  "status": "OUT"
}
```

---

### Test 4: Get Parking Status

```bash
curl http://localhost:8000/api/parking-status
```

**Expected Response:**

```json
{
  "success": true,
  "active_vehicles": 1,
  "vehicles": [
    {
      "uid": "5E6F7G8H",
      "entry_time": "2025-11-24T14:35:00",
      "duration_minutes": 10,
      "fee": 5000.0
    }
  ]
}
```

---

## 📚 API DOCUMENTATION

### Via Swagger UI

Buka di browser: `http://localhost:8000/docs`

Disini Anda bisa:

- ✅ Lihat semua endpoint
- ✅ Test endpoint langsung
- ✅ Lihat request/response format
- ✅ Lihat error codes

### Via ReDoc

Buka di browser: `http://localhost:8000/redoc`

Dokumentasi format yang lebih rapi.

---

## 🖥️ ADMIN DASHBOARD

### Setup Web Admin (dari XAMPP)

1. **Copy folder ke htdocs**

   ```bash
   # Di PowerShell
   Copy-Item -Path "web_admin" -Destination "C:\xampp\htdocs\parking_admin" -Recurse
   ```

2. **Buka di Browser**

   - `http://localhost/parking_admin/`

3. **Features**
   - ✅ Real-time monitoring kendaraan yang parkir
   - ✅ Tampil durasi dan biaya per kendaraan
   - ✅ Auto-refresh setiap 5 detik
   - ✅ Total revenue harian

---

## 🔌 INTEGRASI IoT DEVICE

### Gerbang Masuk - Python Script

Simpan sebagai `gate_entry.py`:

```python
import requests
import time

API_URL = "http://localhost:8000/api/entry"

def read_rfid():
    # TODO: Baca dari sensor RFID Anda
    # Ini adalah mock data untuk testing
    return "1A2B3C4D"

def main():
    uid = read_rfid()
    print(f"📡 UID detected: {uid}")

    try:
        response = requests.post(API_URL, json={"uid": uid})
        data = response.json()

        if data["success"]:
            print(f"✅ Vehicle entry recorded")
            print(f"   Transaction ID: {data['transaction_id']}")
            print(f"   Entry Time: {data['entry_time']}")
            # TODO: Buka gerbang
        else:
            print(f"❌ Error: {data['error']}")
            # TODO: Tampilkan error di LCD/display

    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    main()
```

**Run:**

```bash
python gate_entry.py
```

---

### Gerbang Keluar - Python Script

Simpan sebagai `gate_exit.py`:

```python
import requests

API_URL = "http://localhost:8000/api/exit"

def read_rfid():
    # TODO: Baca dari sensor RFID Anda
    return "1A2B3C4D"

def main():
    uid = read_rfid()
    print(f"📡 UID detected: {uid}")

    try:
        response = requests.post(API_URL, json={"uid": uid})
        data = response.json()

        if data["success"]:
            fee = data["fee"]
            duration = data["duration_minutes"]
            print(f"✅ Vehicle exit recorded")
            print(f"   Biaya Parkir: Rp {fee:,.0f}")
            print(f"   Durasi: {duration} menit")
            # TODO: Buka gerbang + tampilkan biaya di LCD/display
        else:
            print(f"❌ Error: {data['error']}")
            # TODO: Tampilkan error di LCD/display

    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    main()
```

**Run:**

```bash
python gate_exit.py
```

---

## 🐛 TROUBLESHOOTING

### ❌ Error: "Unknown database 'smart_parking_db'"

**Solution:**

```bash
# Buat database dan import schema
mysql -u root -e "CREATE DATABASE smart_parking_db;"
mysql -u root smart_parking_db < database/schema.sql
```

---

### ❌ Error: "Connection refused" atau "Cannot connect to MySQL"

**Check:**

1. XAMPP MySQL running? (lihat Control Panel)
2. Database name di `.env` benar? (`smart_parking_db`)
3. MySQL user/password di `.env` benar?

**Solution:**

```bash
# Test MySQL connection
mysql -u root -e "SELECT VERSION();"
```

---

### ❌ Error: "Port 8000 already in use"

**Solution:**

```bash
# Change port di .env
API_PORT=8001

# Atau kill process yang menggunakan port 8000
# Windows (PowerShell Admin):
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

---

### ❌ Admin Dashboard tidak bisa connect ke API

**Check:**

1. FastAPI server running?
2. URL di `web_admin/script.js` benar?
   ```javascript
   const API_BASE_URL = "http://localhost:8000";
   ```
3. Browser console ada error? (F12 → Console)

**Solution:**

```javascript
// Edit web_admin/script.js
// Change:
const API_BASE_URL = "http://localhost:8000";
// To (jika server di port berbeda):
const API_BASE_URL = "http://localhost:8001";
```

---

## 📊 DATABASE SCHEMA

### vehicles table

```sql
CREATE TABLE vehicles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  uid VARCHAR(50) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### parking_transactions table

```sql
CREATE TABLE parking_transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  uid VARCHAR(50) FOREIGN KEY,
  entry_time DATETIME,
  exit_time DATETIME (nullable),
  duration_minutes INT (nullable),
  fee DECIMAL(10,2) (nullable),
  status ENUM('IN', 'OUT'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### parking_rates table

```sql
CREATE TABLE parking_rates (
  id INT PRIMARY KEY AUTO_INCREMENT,
  base_minutes INT,           -- 60 menit
  base_fee DECIMAL(10,2),     -- Rp 5000
  per_hour_fee DECIMAL(10,2), -- Rp 2000
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 💾 BACKUP & RESTORE DATABASE

### Backup Database

```bash
mysqldump -u root smart_parking_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database

```bash
mysql -u root smart_parking_db < backup_20251124_143000.sql
```

---

## 🚀 PRODUCTION DEPLOYMENT (Cloud)

### 1. Prepare for Cloud

Update `.env` dengan cloud database:

```env
DB_HOST=your-cloud-db.railway.app
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_secure_password
DB_NAME=smart_parking_db
DEBUG=False
API_PORT=8000
```

### 2. Create Procfile

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Deploy ke Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 4. Set Environment Variables di Railway

- Add environment variables dari `.env`
- Connect Railway MySQL database

---

## 📞 QUICK REFERENCE

| Command                           | Purpose              |
| --------------------------------- | -------------------- |
| `python main.py`                  | Start server         |
| `http://localhost:8000/docs`      | API documentation    |
| `http://localhost/parking_admin/` | Admin dashboard      |
| `mysql -u root smart_parking_db`  | Access MySQL         |
| `pip install -r requirements.txt` | Install dependencies |

---

## 📄 FILE STRUCTURE

```
SmartParkingIoT/
├── main.py                      ← Jalankan ini!
├── config.py                    ← Configuration
├── database_connection.py        ← DB connection
├── database/
│   └── schema.sql              ← Import ke MySQL
├── models/
│   └── schemas.py              ← Data models
├── routes/
│   ├── entry.py                ← POST /api/entry
│   ├── exit.py                 ← POST /api/exit
│   └── admin.py                ← GET /api/parking-status
├── utils/
│   └── pricing.py              ← Fee calculation
├── web_admin/                  ← Copy ke htdocs
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env                        ← Configuration (jangan share!)
├── .env.example                ← Template
├── requirements.txt            ← Dependencies
└── README.md                   ← Full documentation
```

---

## ✨ NEXT STEPS

1. ✅ Setup database di XAMPP
2. ✅ Install dependencies
3. ✅ Run FastAPI server
4. ✅ Test API endpoints
5. ✅ Copy web_admin ke htdocs
6. ✅ Integrate dengan IoT device
7. ✅ Monitor via admin dashboard

---

## 📞 CONTACT & SUPPORT

Untuk pertanyaan atau issue:

- Check README.md untuk dokumentasi lengkap
- Lihat API docs di `http://localhost:8000/docs`
- Enable DEBUG mode di `.env` untuk verbose logging

---

**Happy Parking! 🅿️**

Last Updated: November 24, 2025
