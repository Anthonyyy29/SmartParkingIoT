# 📖 PANDUAN SETUP - SMART PARKING IOT BACKEND

Panduan step-by-step untuk setup dan menjalankan Smart Parking IoT Backend API.

**Status:** ✅ Verified & Teruji  
**Waktu Setup:** ~20 menit  
**Level:** Beginner-friendly

---

## 📋 REQUIREMENTS

### Software yang Dibutuhkan:

- Windows 10/11
- XAMPP (dengan MySQL)
- Python 3.12.1+
- Text editor (VS Code recommended)
- Browser modern (Chrome/Firefox/Edge)

### Pengetahuan Dasar:

- Command line / Terminal
- MySQL basics
- Python basics
- REST API concepts (optional tapi membantu)

---

## STEP 1️⃣ - SETUP DATABASE

### A. Buka phpMyAdmin

1. Pastikan XAMPP berjalan (MySQL harus "Running")
2. Buka browser, ketik: `http://localhost/phpmyadmin/`
3. Login (default: username=`root`, password=kosong)

### B. Buat Database Baru

1. Klik tab **"Databases"**
2. Di bagian **"Create database"**, ketik: `smart_parking_db`
3. Pilih character set: `utf8mb4_general_ci`
4. Klik tombol **"Create"**

✅ Database berhasil dibuat!

### C. Import Schema SQL

1. Klik database **`smart_parking_db`** yang baru dibuat
2. Klik tab **"Import"**
3. Klik **"Choose File"** dan pilih: `database/schema.sql`
4. Scroll ke bawah, klik **"Import"**

✅ Schema sudah diimport! Seharusnya ada 3 tabel:

- `parking_rates`
- `parking_transactions`
- `vehicles`

### D. Verifikasi Database

```bash
# Terminal / Command Prompt
mysql -u root smart_parking_db -e "SHOW TABLES;"
```

Expected output:

```
parking_rates
parking_transactions
vehicles
```

---

## STEP 2️⃣ - SETUP PYTHON ENVIRONMENT

### A. Buka Terminal/PowerShell

1. Buka folder project
2. Klik kanan, pilih **"Open PowerShell here"**
   atau jalankan:
   ```bash
   cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
   ```

### B. Verifikasi Python

```bash
python --version
```

Expected: `Python 3.12.1` (atau versi 3.12.x lainnya)

### C. Install Dependencies

```bash
pip install -r requirements.txt
```

Proses ini akan menginstall:

- FastAPI 0.104.1
- Uvicorn 0.24.0
- MySQL connector
- Pydantic
- Dan dependensi lainnya

⏳ Tunggu sampai selesai (~2-3 menit)

✅ Semua dependencies sudah terinstall!

---

## STEP 3️⃣ - KONFIGURASI ENVIRONMENT

### A. Buka File `.env`

Buka file `.env` di folder project dengan text editor

### B. Verifikasi Konfigurasi

Pastikan konfigurasi sesuai dengan setup lokal Anda:

```env
# Database Configuration
DB_HOST=localhost          # ✅ Biarkan default
DB_PORT=3306              # ✅ Biarkan default
DB_USER=root              # ✅ Default XAMPP
DB_PASSWORD=              # ✅ Kosong (default XAMPP)
DB_NAME=smart_parking_db  # ✅ Sesuai database yang dibuat

# FastAPI Configuration
API_HOST=0.0.0.0          # ✅ Biarkan default
API_PORT=8000             # ✅ Biarkan default
DEBUG=True                # ✅ True untuk development
```

### C. Jika Berbeda dengan Default

**Jika MySQL Anda menggunakan password:**

```env
DB_PASSWORD=your_password_here
```

**Jika ingin ganti port API:**

```env
API_PORT=8001
```

✅ Konfigurasi selesai!

---

## STEP 4️⃣ - JALANKAN SERVER

### A. Buka Terminal di Folder Project

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
```

### B. Jalankan FastAPI Server

```bash
python main.py
```

### C. Verifikasi Server Berjalan

Expected output:

```
🚀 Starting Smart Parking IoT API...
✅ Connected to smart_parking_db database
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Server berhasil berjalan!**

**JANGAN TUTUP TERMINAL INI!** Biarkan berjalan di background.

---

## STEP 5️⃣ - TEST API

### A. Buka Swagger UI

1. Buka browser
2. Ketik: `http://localhost:8000/docs`
3. Seharusnya muncul Swagger UI yang cantik

### B. Test Health Check

1. Scroll ke endpoint **`GET /health`**
2. Klik tombol **"Try it out"**
3. Klik tombol **"Execute"**

Expected response:

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-24T..."
}
```

✅ API berhasil terhubung ke database!

### C. Test Entry Endpoint

1. Scroll ke **`POST /api/entry`**
2. Klik **"Try it out"**
3. Di Request body, ubah UID, contoh:
   ```json
   {
     "uid": "TEST001"
   }
   ```
4. Klik **"Execute"**

Expected response:

```json
{
  "success": true,
  "message": "Vehicle entry recorded successfully",
  "transaction_id": 1,
  "entry_time": "2025-11-24T14:30:00"
}
```

✅ Entry berhasil dicatat!

### D. Test Exit Endpoint

1. Scroll ke **`POST /api/exit`**
2. Klik **"Try it out"**
3. Gunakan UID yang sama:
   ```json
   {
     "uid": "TEST001"
   }
   ```
4. Klik **"Execute"**

Expected response:

```json
{
  "success": true,
  "message": "Vehicle exit recorded successfully",
  "fee": 5000,
  "duration_minutes": 45,
  "status": "OUT"
}
```

✅ Exit berhasil dan biaya sudah dihitung!

---

## STEP 6️⃣ - SETUP ADMIN DASHBOARD

### A. Copy Folder web_admin ke htdocs

Buka File Explorer:

1. Navigasi ke: `C:\xampp\htdocs\`
2. Buat folder baru: `parking_admin`
3. Copy semua file dari `web_admin/` ke sana

Atau via command:

```bash
xcopy web_admin C:\xampp\htdocs\parking_admin /E /I
```

### B. Buka Admin Dashboard

1. Buka browser
2. Ketik: `http://localhost/parking_admin/`
3. Seharusnya muncul dashboard yang cantik

### C. Test Dashboard

1. Di dashboard, klik tombol **"Refresh"**
2. Seharusnya tampil kendaraan yang sedang parkir
3. Klik **"Auto Refresh: OFF"** untuk enable auto-refresh

✅ Admin dashboard berhasil disetup!

---

## 🧪 VERIFICATION CHECKLIST

Sebelum mulai development, pastikan semua ini OK:

- [ ] Database `smart_parking_db` sudah dibuat
- [ ] 3 tabel ada di database (cek via phpMyAdmin)
- [ ] Python 3.12.1+ terinstall
- [ ] Dependencies sudah diinstall (`pip list`)
- [ ] FastAPI server berjalan tanpa error
- [ ] Swagger UI bisa diakses (`http://localhost:8000/docs`)
- [ ] Health check endpoint responding
- [ ] Entry endpoint bisa mencatat kendaraan masuk
- [ ] Exit endpoint bisa mencatat keluar dan hitung biaya
- [ ] Admin dashboard bisa di-refresh

Jika semua checklist sudah ✅, berarti **setup selesai dan siap development!**

---

## 🐛 TROUBLESHOOTING

### Problem: "Database not found"

```
mysql.connector.errors.ProgrammingError: 1049 (42000): Unknown database 'smart_parking_db'
```

**Solution:**

1. Buka phpMyAdmin
2. Create database `smart_parking_db`
3. Import `database/schema.sql`

---

### Problem: "Connection refused"

```
ConnectionRefusedError: [Errno 10061] No connection could be made
```

**Solution:**

1. Pastikan MySQL di XAMPP sudah "Running"
2. Cek .env file, DB_HOST dan DB_PORT benar
3. Cek DB_USER dan DB_PASSWORD benar

---

### Problem: "Port 8000 already in use"

```
OSError: [Errno 10048] Only one usage of each socket address
```

**Solution:**

```bash
# Option 1: Kill process yang menggunakan port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 2: Ubah port di .env
# API_PORT=8001
```

---

### Problem: "Module not found"

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**

```bash
# Pastikan sudah di folder project
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem: Admin dashboard tidak connect ke API

**Solution:**

1. Buka `web_admin/script.js`
2. Cek variable `API_BASE_URL`
3. Pastikan sama dengan server URL (default `http://localhost:8000`)

---

## ✅ SELESAI!

Setup sudah selesai! 🎉

Sekarang Anda bisa:

1. Develop API endpoints
2. Test dengan Swagger UI
3. Monitor dengan admin dashboard
4. Integrasi dengan IoT device

---

## 📚 NEXT STEPS

1. Baca: `QUICK_REFERENCE.md` (quick tips)
2. Pelajari: `iot_client_example.py` (IoT integration)
3. Deploy: `README.md` bagian Cloud Deployment

---

**Pertanyaan? Lihat troubleshooting section atau README.md!**

Happy Coding! 🚀
