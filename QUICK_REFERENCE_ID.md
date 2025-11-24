# ⚡ QUICK REFERENCE - SMART PARKING IOT

Panduan cepat untuk command, endpoints, dan troubleshooting.

---

## 🚀 STARTUP COMMANDS

### Jalankan Server

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
python main.py
```

Expected:

```
🚀 Starting Smart Parking IoT API...
✅ Connected to smart_parking_db database
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Jalankan Di Background (PowerShell)

```bash
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

### Stop Server

```
Ctrl + C (di terminal)
```

---

## 🔗 QUICK URLS

| Service             | URL                               | Note                 |
| ------------------- | --------------------------------- | -------------------- |
| **API Base**        | `http://localhost:8000`           | REST API             |
| **Swagger UI**      | `http://localhost:8000/docs`      | Interactive docs     |
| **Health Check**    | `http://localhost:8000/health`    | Test connection      |
| **phpMyAdmin**      | `http://localhost/phpmyadmin/`    | Database management  |
| **Admin Dashboard** | `http://localhost/parking_admin/` | Monitoring dashboard |

---

## 🔌 ENDPOINTS REFERENCE

| Method | Endpoint                      | Purpose             | Returns                       |
| ------ | ----------------------------- | ------------------- | ----------------------------- |
| POST   | `/api/entry`                  | Record entry        | transaction_id, entry_time    |
| POST   | `/api/exit`                   | Record exit         | fee, duration_minutes         |
| GET    | `/api/parking-status`         | All active vehicles | vehicles list, total_vehicles |
| GET    | `/api/last-transaction/{uid}` | Last transaction    | transaction details           |
| GET    | `/health`                     | Health check        | status, database connection   |

---

## 📝 QUICK TEST EXAMPLES

### Test Entry

**PowerShell:**

```powershell
$body = @{ uid = "TEST001" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/entry" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

**Command Prompt:**

```bash
curl -X POST http://localhost:8000/api/entry ^
  -H "Content-Type: application/json" ^
  -d "{\"uid\":\"TEST001\"}"
```

**Browser (Swagger UI):**

1. Buka `http://localhost:8000/docs`
2. Cari endpoint POST /api/entry
3. Klik "Try it out"
4. Masukkan `{"uid":"TEST001"}`
5. Klik "Execute"

---

### Test Exit

```bash
curl -X POST http://localhost:8000/api/exit ^
  -H "Content-Type: application/json" ^
  -d "{\"uid\":\"TEST001\"}"
```

---

### Check Parking Status

```bash
curl http://localhost:8000/api/parking-status
```

---

### Check Health

```bash
curl http://localhost:8000/health
```

---

## 💲 PRICING QUICK REFERENCE

**Formula:** `5000 + (ceil(durasi/60) - 1) × 2000`

| Duration    | Fee       |
| ----------- | --------- |
| 1-60 min    | Rp 5.000  |
| 61-120 min  | Rp 7.000  |
| 121-180 min | Rp 9.000  |
| 181-240 min | Rp 11.000 |
| 241-300 min | Rp 13.000 |

---

## 🐛 QUICK TROUBLESHOOTING

### ❌ "Connection refused"

**Penyebab:** MySQL atau server tidak running

**Fix:**

```bash
# Cek MySQL status
netstat -ano | findstr :3306

# Jika tidak ada, start XAMPP MySQL
# Buka XAMPP Control Panel, start MySQL
```

---

### ❌ "Port already in use"

**Penyebab:** Port 8000 sudah dipakai

**Fix Option 1 - Kill process:**

```powershell
# Cari process di port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill process
taskkill /PID <PID> /F
```

**Fix Option 2 - Ubah port:**

```env
# .env
API_PORT=8001
```

---

### ❌ "Database not found"

**Penyebab:** Database belum dibuat

**Fix:**

```bash
# Via MySQL command
mysql -u root -e "CREATE DATABASE smart_parking_db;"

# Atau via phpMyAdmin
# 1. Buka http://localhost/phpmyadmin/
# 2. Klik "Databases"
# 3. Buat database "smart_parking_db"
```

---

### ❌ "Table doesn't exist"

**Penyebab:** Schema belum diimport

**Fix:**

```bash
# Import schema
mysql -u root smart_parking_db < database/schema.sql

# Atau via phpMyAdmin
# 1. Pilih database smart_parking_db
# 2. Klik "Import"
# 3. Pilih file database/schema.sql
# 4. Klik "Import"
```

---

### ❌ "Module not found"

**Penyebab:** Dependencies belum diinstall

**Fix:**

```bash
# Install dependencies
pip install -r requirements.txt
```

---

### ❌ "ALREADY_PARKED error"

**Penyebab:** Kendaraan sudah entry, coba entry lagi

**Fix:**

```bash
# Exit dulu dengan UID yang sama
curl -X POST http://localhost:8000/api/exit ^
  -H "Content-Type: application/json" ^
  -d "{\"uid\":\"TEST001\"}"

# Baru coba entry lagi
```

---

### ❌ "NOT_FOUND error saat exit"

**Penyebab:** UID tidak ada atau sudah exit

**Fix:**

```bash
# Cek history transaksi
curl http://localhost:8000/api/last-transaction/TEST001

# Jika status = "OUT", kendaraan sudah exit
# Entry dulu sebelum exit
```

---

## 🔧 COMMON OPERATIONS

### View Database

```bash
# Connect ke database
mysql -u root smart_parking_db

# Di MySQL prompt:
# View all vehicles
SELECT * FROM vehicles;

# View all transactions
SELECT * FROM parking_transactions;

# View parking rates
SELECT * FROM parking_rates;

# Exit
EXIT;
```

---

### Clear Database (Reset)

```bash
# HATI-HATI! Ini akan hapus semua data

mysql -u root -e "USE smart_parking_db; TRUNCATE TABLE parking_transactions; TRUNCATE TABLE vehicles;"
```

---

### Check Current Parked Vehicles

```bash
mysql -u root smart_parking_db -e "SELECT uid, entry_time FROM parking_transactions WHERE status='IN';"
```

---

### View Parking Revenue Today

```bash
mysql -u root smart_parking_db -e "SELECT SUM(fee) as total_fee FROM parking_transactions WHERE status='OUT' AND DATE(exit_time)=CURDATE();"
```

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Sebelum deploy ke production:

- [ ] `.env` sudah dikonfigurasi untuk production
- [ ] Database credentials benar
- [ ] Semua endpoints tested via Swagger UI
- [ ] Admin dashboard bisa diakses
- [ ] No hardcoded sensitive data (passwords, keys)
- [ ] CORS origins sudah diupdate untuk production domain
- [ ] Error logs bisa diaccess untuk monitoring

---

## 🚀 DEPLOYMENT QUICK START

### Local (Development)

```bash
python main.py
```

### Production (Railway/Render)

```bash
# Gunakan gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Docker (Optional)

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## 📚 FULL DOCUMENTATION

- **Setup:** `SETUP_GUIDE_ID.md`
- **API:** `README_ID.md`
- **Project Overview:** `PROJECT_SUMMARY_ID.md`
- **Testing:** `DEPLOYMENT_CHECKLIST_ID.md`
- **Project Stats:** `00_START_HERE_ID.md`

---

## 💡 TIPS

1. **Auto-refresh Admin Dashboard:** Klik tombol "Auto Refresh" untuk monitor real-time
2. **Test dengan Swagger:** Lebih mudah dari manual curl
3. **Check logs di console:** Lihat error details di terminal tempat server running
4. **Monitor database:** Buka phpMyAdmin untuk lihat data langsung
5. **Use postman:** Install Postman untuk test dan organize API requests

---

**Last Updated:** 2025-11-24  
**Status:** ✅ Production Ready

Happy Coding! 🚀
