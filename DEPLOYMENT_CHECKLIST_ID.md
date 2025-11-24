# ✅ DEPLOYMENT CHECKLIST - SMART PARKING IOT

Panduan lengkap untuk testing, validation, dan deployment Smart Parking IoT Backend.

**Purpose:** Memastikan sistem siap production sebelum go-live  
**Target:** Operator Parkir, System Administrator, DevOps Engineer

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Phase 1: Environment Setup ✓

- [ ] Python 3.12.1+ terinstall

  ```bash
  python --version
  # Expected: Python 3.12.1
  ```

- [ ] XAMPP MySQL running

  - [ ] Buka XAMPP Control Panel
  - [ ] Klik "Start" untuk MySQL
  - [ ] Status harus "Running" (hijau)

- [ ] Database `smart_parking_db` dibuat

  ```bash
  mysql -u root -e "USE smart_parking_db; SHOW TABLES;"
  # Should show: 3 tables (vehicles, parking_transactions, parking_rates)
  ```

- [ ] Dependencies terinstall

  ```bash
  pip list | findstr fastapi
  # Expected: fastapi 0.104.1
  ```

- [ ] `.env` file dikonfigurasi dengan benar
  ```env
  DB_HOST=localhost
  DB_USER=root
  DB_PASSWORD=          (kosong untuk default XAMPP)
  DB_NAME=smart_parking_db
  API_PORT=8000
  ```

---

### Phase 2: Backend Testing ✓

#### Test 1: Server Startup

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
python main.py
```

✅ Expected Output:

```
🚀 Starting Smart Parking IoT API...
✅ Connected to smart_parking_db database
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

- [ ] Server berhasil start tanpa error
- [ ] Database connection successful
- [ ] No error messages di console

---

#### Test 2: Health Check Endpoint

```bash
curl http://localhost:8000/health
```

✅ Expected Response:

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-24T14:30:00"
}
```

- [ ] Response status 200
- [ ] Database connection: "connected"
- [ ] Valid timestamp

---

#### Test 3: Swagger UI Documentation

**URL:** `http://localhost:8000/docs`

- [ ] Swagger UI loading tanpa error
- [ ] Semua 5 endpoints terlihat:
  - [ ] `GET /health`
  - [ ] `POST /api/entry`
  - [ ] `POST /api/exit`
  - [ ] `GET /api/parking-status`
  - [ ] `GET /api/last-transaction/{uid}`
- [ ] Setiap endpoint punya dokumentasi lengkap
- [ ] Request/response schemas terlihat

---

### Phase 3: API Endpoint Testing ✓

#### Test A: POST /api/entry (Vehicle Entry)

**Step 1:** Buka Swagger UI → POST /api/entry → "Try it out"

**Input:**

```json
{
  "uid": "TEST_CAR_001"
}
```

- [ ] Response status 200
- [ ] `success: true`
- [ ] `transaction_id` ada dan numeric
- [ ] `entry_time` format datetime
- [ ] `vehicle_status: "IN"`

**Step 2:** Test dengan UID berbeda

```json
{
  "uid": "TEST_CAR_002"
}
```

- [ ] Berhasil record entry kedua
- [ ] Transaction ID berbeda dengan pertama

**Step 3:** Test duplikat entry (should fail)

Coba entry lagi dengan UID yang sama:

```json
{
  "uid": "TEST_CAR_001"
}
```

- [ ] Response status 400
- [ ] `success: false`
- [ ] `error_code: "ALREADY_PARKED"`
- [ ] Message mencakup UID yang sudah parkir

---

#### Test B: GET /api/parking-status (Active Vehicles)

**Action:** GET /api/parking-status (tanpa parameter)

✅ Expected Response:

```json
{
  "success": true,
  "timestamp": "2025-11-24T14:35:00",
  "total_vehicles_parked": 2,
  "vehicles": [
    {
      "uid": "TEST_CAR_001",
      "entry_time": "2025-11-24T14:30:00.000000",
      "duration_minutes": 5,
      "current_fee": 5000,
      "current_fee_formatted": "Rp 5.000"
    },
    {
      "uid": "TEST_CAR_002",
      "entry_time": "2025-11-24T14:32:00.000000",
      "duration_minutes": 3,
      "current_fee": 5000,
      "current_fee_formatted": "Rp 5.000"
    }
  ]
}
```

- [ ] Response status 200
- [ ] `total_vehicles_parked` sesuai (2)
- [ ] Kedua vehicle terlihat dalam list
- [ ] Duration minutes meningkat setiap kali di-call (real-time)
- [ ] Fee calculated correctly untuk masing-masing

---

#### Test C: POST /api/exit (Vehicle Exit & Fee Calculation)

**Step 1:** Exit dengan UID pertama

Input:

```json
{
  "uid": "TEST_CAR_001"
}
```

✅ Expected Response:

```json
{
  "success": true,
  "message": "Vehicle exit recorded successfully",
  "uid": "TEST_CAR_001",
  "transaction_id": 1,
  "entry_time": "2025-11-24T14:30:00.000000",
  "exit_time": "2025-11-24T14:45:00.000000",
  "duration_minutes": 15,
  "fee": 5000,
  "fee_formatted": "Rp 5.000",
  "vehicle_status": "OUT"
}
```

- [ ] Response status 200
- [ ] `success: true`
- [ ] `exit_time` ada dan lebih besar dari `entry_time`
- [ ] `duration_minutes` realistic (15 menit)
- [ ] `fee: 5000` (< 60 menit = base fee)
- [ ] `vehicle_status: "OUT"`

**Step 2:** Verify parking status updated

Panggil GET /api/parking-status lagi:

- [ ] `total_vehicles_parked` berkurang menjadi 1
- [ ] TEST_CAR_001 tidak ada di list lagi
- [ ] TEST_CAR_002 masih ada

**Step 3:** Test exit dengan UID tidak ada (should fail)

Input:

```json
{
  "uid": "NONEXISTENT"
}
```

- [ ] Response status 400 atau 404
- [ ] `success: false`
- [ ] `error_code: "NOT_FOUND"`

---

#### Test D: GET /api/last-transaction/{uid} (Transaction History)

**Step 1:** Get last transaction dari kendaraan yang sudah exit

```
GET /api/last-transaction/TEST_CAR_001
```

✅ Expected Response:

```json
{
  "success": true,
  "uid": "TEST_CAR_001",
  "transaction_id": 1,
  "status": "OUT",
  "entry_time": "2025-11-24T14:30:00.000000",
  "exit_time": "2025-11-24T14:45:00.000000",
  "duration_minutes": 15,
  "fee": 5000,
  "fee_formatted": "Rp 5.000",
  "message": "Vehicle successfully exited"
}
```

- [ ] Response status 200
- [ ] `status: "OUT"` (sudah exit)
- [ ] Fee ada dan sesuai
- [ ] All fields populated

**Step 2:** Get last transaction dari kendaraan masih parkir

```
GET /api/last-transaction/TEST_CAR_002
```

✅ Expected Response:

```json
{
  "success": true,
  "uid": "TEST_CAR_002",
  "status": "IN",
  "entry_time": "2025-11-24T14:32:00.000000",
  "exit_time": null,
  "duration_minutes": null,
  "fee": null,
  "message": "Vehicle is currently parked"
}
```

- [ ] Response status 200
- [ ] `status: "IN"` (masih parkir)
- [ ] `exit_time: null`, `fee: null`
- [ ] Message indicates "currently parked"

**Step 3:** Get last transaction dari UID tidak ada (should fail)

```
GET /api/last-transaction/UNKNOWN
```

- [ ] Response status 404
- [ ] `success: false`
- [ ] `error_code: "NOT_FOUND"`

---

### Phase 4: Pricing Formula Validation ✓

Test pricing dengan berbagai durasi:

#### Test Case 1: Less than 1 hour

- Entry: 14:30
- Exit: 14:45 (15 minutes)
- Expected Fee: **Rp 5.000** ✓

- [ ] Fee matches expected

#### Test Case 2: Exactly 1 hour

- Entry: 14:30
- Exit: 15:30 (60 minutes)
- Expected Fee: **Rp 5.000** ✓

- [ ] Fee matches expected

#### Test Case 3: Between 1-2 hours

- Entry: 14:30
- Exit: 15:45 (75 minutes)
- Expected Fee: **Rp 7.000** (ceil(75/60)=2 jam) ✓

- [ ] Fee matches expected

#### Test Case 4: Exactly 2 hours

- Entry: 14:30
- Exit: 16:30 (120 minutes)
- Expected Fee: **Rp 7.000** ✓

- [ ] Fee matches expected

#### Test Case 5: More than 2 hours

- Entry: 14:30
- Exit: 17:30 (180 minutes)
- Expected Fee: **Rp 9.000** (ceil(180/60)=3 jam) ✓

- [ ] Fee matches expected

---

### Phase 5: Database Integrity Testing ✓

#### Test 1: Check vehicles table

```bash
mysql -u root smart_parking_db -e "SELECT * FROM vehicles;"
```

- [ ] Should show all entered vehicles
- [ ] UID values correct
- [ ] No duplicate UIDs

#### Test 2: Check parking_transactions table

```bash
mysql -u root smart_parking_db -e "SELECT * FROM parking_transactions;"
```

- [ ] All entries recorded
- [ ] Status = 'IN' atau 'OUT' correct
- [ ] Fee calculated for 'OUT' records
- [ ] entry_time before exit_time (jika ada)

#### Test 3: Check foreign keys

```bash
mysql -u root smart_parking_db -e "SHOW CREATE TABLE parking_transactions\G"
```

- [ ] Foreign key constraint ada
- [ ] References vehicles(uid)
- [ ] ON DELETE CASCADE configured

#### Test 4: Check indexes

```bash
mysql -u root smart_parking_db -e "SHOW INDEXES FROM parking_transactions;"
```

- [ ] Index pada `uid`
- [ ] Index pada `entry_time`
- [ ] Index pada `status`

---

### Phase 6: Admin Dashboard Testing ✓

#### Setup Admin Dashboard

1. Copy folder `web_admin/` ke `C:\xampp\htdocs\parking_admin\`
2. Buka: `http://localhost/parking_admin/`

- [ ] Dashboard loading tanpa error
- [ ] Layout responsive
- [ ] No console errors (buka DevTools → Console)

#### Test Dashboard Features

**Feature 1: Display Active Vehicles**

- [ ] Kendaraan yang masih parkir terlihat di tabel
- [ ] Kolom: UID, Duration, Current Fee
- [ ] Data akurat

**Feature 2: Refresh Button**

- [ ] Klik tombol "Refresh"
- [ ] Data update dari API
- [ ] Durasi berubah (real-time)
- [ ] Fee terupdate

**Feature 3: Auto-Refresh**

- [ ] Klik "Auto Refresh: OFF" → ON
- [ ] Data auto-update setiap 5 detik
- [ ] Durasi meningkat setiap refresh
- [ ] Klik OFF untuk stop auto-refresh

**Feature 4: Status Cards**

- [ ] "Total Vehicles Parked" card menampilkan angka
- [ ] "Total Daily Revenue" card menampilkan jumlah uang
- [ ] Angka terupdate saat refresh

**Feature 5: Error Handling**

- [ ] Buka DevTools → Network tab
- [ ] Verifikasi requests ke `/api/parking-status`
- [ ] Response time reasonable (< 1 detik)

---

### Phase 7: Error Handling & Edge Cases ✓

#### Test 1: Invalid UID

Try entry dengan UID kosong:

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid":""}'
```

- [ ] Status 400
- [ ] Error code: `INVALID_UID`
- [ ] Proper error message

#### Test 2: UID too long

Try entry dengan UID > 50 karakter:

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid":"'$(printf 'A%.0s' {1..51})'"}'
```

- [ ] Status 400
- [ ] Error code: `INVALID_UID`
- [ ] Message mencakup length requirement

#### Test 3: Concurrent Requests

Jalankan 5 entry requests bersamaan:

```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/entry \
    -H "Content-Type: application/json" \
    -d "{\"uid\":\"CONCURRENT_$i\"}" &
done
```

- [ ] Semua request succeed (5 vehicles)
- [ ] Tidak ada duplicate transaction IDs
- [ ] Database consistent

#### Test 4: Rapid Exit Without Entry

Try exit dengan UID yang belum entry:

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid":"NEVER_ENTERED"}'
```

- [ ] Status 400 atau 404
- [ ] Error code: `NOT_FOUND`
- [ ] Clear error message

#### Test 5: Double Exit

Entry, exit, then exit again dengan UID sama:

```bash
# Entry
curl -X POST http://localhost:8000/api/entry \
  -d '{"uid":"DOUBLE_EXIT_TEST"}'

# Exit 1
curl -X POST http://localhost:8000/api/exit \
  -d '{"uid":"DOUBLE_EXIT_TEST"}'

# Exit 2 (should fail)
curl -X POST http://localhost:8000/api/exit \
  -d '{"uid":"DOUBLE_EXIT_TEST"}'
```

- [ ] Second exit fails
- [ ] Error code: `NOT_FOUND`
- [ ] First exit successful dengan correct fee

---

### Phase 8: Performance Testing ✓

#### Test 1: Response Time

Test `/api/parking-status` response time:

```bash
# PowerShell
Measure-Command {
  curl http://localhost:8000/api/parking-status
}
```

- [ ] Response time < 1 second
- [ ] Acceptable untuk real-time dashboard

#### Test 2: Load Testing (10 concurrent requests)

```bash
for i in {1..10}; do
  curl http://localhost:8000/api/parking-status &
done
```

- [ ] All requests success
- [ ] Server tidak crash
- [ ] Responses consistent

#### Test 3: Load Testing (100 entries)

Insert 100 vehicles:

```python
import requests
import time

start = time.time()
for i in range(100):
    requests.post(
        "http://localhost:8000/api/entry",
        json={"uid": f"LOAD_TEST_{i}"}
    )
end = time.time()
```

- [ ] Semua entry berhasil (status 200 atau 400 jika duplikat)
- [ ] Time taken < 30 seconds
- [ ] Database tidak crash
- [ ] Dashboard masih responsive

---

### Phase 9: CORS & Security ✓

#### Test 1: CORS Headers

```bash
curl -i -X OPTIONS http://localhost:8000/api/entry \
  -H "Origin: http://localhost:3000"
```

- [ ] Response includes: `Access-Control-Allow-Origin`
- [ ] Allows localhost origins

#### Test 2: SQL Injection Prevention

Try entry dengan SQL injection payload:

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid":"TEST; DROP TABLE vehicles; --"}'
```

- [ ] Payload treated as normal string
- [ ] No error in database
- [ ] Database intact (not dropped)

---

### Phase 10: Data Persistence ✓

#### Test 1: Server Restart

1. Test entry/exit (record beberapa transactions)
2. Buka MySQL query dan lihat data:
   ```bash
   mysql -u root smart_parking_db -e "SELECT * FROM parking_transactions;"
   ```
3. Stop server (Ctrl+C)
4. Start server lagi (python main.py)
5. Query lagi data:
   ```bash
   mysql -u root smart_parking_db -e "SELECT * FROM parking_transactions;"
   ```

- [ ] Data tetap ada setelah server restart
- [ ] No data loss
- [ ] Transaction history preserved

---

## 📋 PRODUCTION READINESS CHECKLIST

Before deploying to production, verify:

### Configuration

- [ ] `.env` configured untuk production environment
- [ ] Database credentials aman (tidak hardcoded)
- [ ] API_PORT sesuai dengan server setup
- [ ] No debug mode enabled di production

### Security

- [ ] Update CORS origins ke production domain saja
- [ ] Consider adding API key authentication
- [ ] Enable HTTPS untuk production URL
- [ ] Rate limiting configured
- [ ] Input validation comprehensive

### Performance

- [ ] Database indexes created dan verified
- [ ] Connection pooling configured
- [ ] Caching strategy implemented (jika perlu)
- [ ] Load testing passed

### Monitoring

- [ ] Logging setup untuk error tracking
- [ ] Database backup strategy defined
- [ ] Monitoring dashboard setup (optional)
- [ ] Alert system configured (optional)

### Documentation

- [ ] API documentation updated
- [ ] Deployment guide created
- [ ] Troubleshooting guide created
- [ ] Team trained on system operation

---

## 🚀 DEPLOYMENT SIGN-OFF

**When ready for production deployment, fill out:**

| Item                   | Status | Checked By   | Date     |
| ---------------------- | ------ | ------------ | -------- |
| All tests passed       | ✅     | ****\_\_**** | **\_\_** |
| Performance acceptable | ✅     | ****\_\_**** | **\_\_** |
| Security reviewed      | ✅     | ****\_\_**** | **\_\_** |
| Documentation complete | ✅     | ****\_\_**** | **\_\_** |
| Team trained           | ✅     | ****\_\_**** | **\_\_** |

---

## 🆘 TROUBLESHOOTING DURING TESTING

### Issue: "Cannot connect to database"

**Solution:**

- Verify MySQL running: `netstat -ano | findstr :3306`
- Check credentials dalam .env
- Verify database exists: `mysql -u root -e "USE smart_parking_db;"`

---

### Issue: "Port 8000 already in use"

**Solution:**

- Find process: `Get-NetTCPConnection -LocalPort 8000`
- Kill process: `taskkill /PID <PID> /F`
- Or change port in .env: `API_PORT=8001`

---

### Issue: "Module not found"

**Solution:**

- Reinstall: `pip install -r requirements.txt`
- Verify installation: `pip list`

---

### Issue: "Dashboard tidak connect ke API"

**Solution:**

- Verify API running: `curl http://localhost:8000/health`
- Check `web_admin/script.js` for correct `API_BASE_URL`
- Open DevTools console untuk error details

---

## ✅ TESTING COMPLETE!

Jika semua checklist sudah ✅, sistem siap untuk:

1. Live deployment
2. IoT device integration
3. Production usage

---

**Last Updated:** 2025-11-24  
**Version:** 1.0.0  
**Status:** ✅ PRODUCTION READY

Happy Deployment! 🚀
