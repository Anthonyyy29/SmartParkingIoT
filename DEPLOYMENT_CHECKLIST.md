# ✅ DEPLOYMENT CHECKLIST

Smart Parking IoT Backend - Deployment & Testing Checklist

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### Database Setup

- [ ] XAMPP MySQL running
- [ ] Database `smart_parking_db` created
- [ ] `database/schema.sql` imported
- [ ] Verify 3 tables exist: `vehicles`, `parking_transactions`, `parking_rates`

**Test:**

```bash
mysql -u root smart_parking_db -e "SHOW TABLES;"
```

Expected output:

```
parking_rates
parking_transactions
vehicles
```

---

### Python Environment

- [ ] Python 3.12.1 installed
- [ ] `pip install -r requirements.txt` completed successfully
- [ ] All packages installed correctly

**Test:**

```bash
pip list | findstr fastapi
```

Expected: `fastapi 0.104.1`

---

### Configuration

- [ ] `.env` file created (already done ✅)
- [ ] DB_HOST, DB_USER, DB_PASSWORD verified
- [ ] API_PORT set to 8000 (or your preferred port)
- [ ] DEBUG set to True (for development)

---

## 🚀 STARTUP SEQUENCE

### Step 1: Start XAMPP

```bash
# Start XAMPP Control Panel
# Click: Start for Apache and MySQL
```

✅ Wait until MySQL shows "Running"

### Step 2: Verify MySQL Connection

```bash
mysql -u root -e "SELECT VERSION();"
```

Expected: `mysql Ver 8.x.x for Windows on x86_64`

### Step 3: Start FastAPI Server

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
python main.py
```

Expected output:

```
🚀 Starting Smart Parking IoT API...
✅ Connected to smart_parking_db database
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 API TESTING CHECKLIST

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

- [ ] Response code: 200
- [ ] Contains "healthy" and "connected"

---

### Test 2: Entry Endpoint

**Request:**

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid": "TEST001"}'
```

- [ ] Response code: 200
- [ ] success = true
- [ ] transaction_id > 0
- [ ] entry_time exists

**Check Database:**

```bash
mysql -u root smart_parking_db -e "SELECT * FROM parking_transactions;"
```

- [ ] 1 row with status='IN'
- [ ] entry_time is current time

---

### Test 3: Entry with Duplicate UID

**Request (same UID as Test 2):**

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid": "TEST001"}'
```

- [ ] Response code: 200
- [ ] success = false
- [ ] error = "Vehicle is already in parking"
- [ ] code = "ALREADY_PARKED"

---

### Test 4: Exit Endpoint

**Request:**

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid": "TEST001"}'
```

- [ ] Response code: 200
- [ ] success = true
- [ ] status = "OUT"
- [ ] fee > 0
- [ ] duration_minutes > 0

**Verify Fee Calculation:**

- [ ] If duration < 60 min → fee = 5000
- [ ] If duration 60-120 min → fee = 7000
- [ ] If duration > 120 min → fee = 9000+

---

### Test 5: Exit with Non-existent UID

**Request:**

```bash
curl -X POST http://localhost:8000/api/exit \
  -H "Content-Type: application/json" \
  -d '{"uid": "NONEXISTENT"}'
```

- [ ] Response code: 200
- [ ] success = false
- [ ] error = "Vehicle not found in parking"
- [ ] code = "NOT_FOUND"

---

### Test 6: Parking Status

**Request:**

```bash
curl http://localhost:8000/api/parking-status
```

- [ ] Response code: 200
- [ ] success = true
- [ ] active_vehicles >= 0
- [ ] vehicles array contains all IN status records

---

### Test 7: Last Transaction Query

**Request:**

```bash
curl http://localhost:8000/api/last-transaction/TEST001
```

- [ ] Response code: 200
- [ ] success = true
- [ ] uid = "TEST001"
- [ ] status = "OUT" (from Test 4)
- [ ] fee contains parking cost

---

### Test 8: API Documentation

- [ ] Open `http://localhost:8000/docs`
- [ ] Swagger UI loads
- [ ] Can see all endpoints
- [ ] Can test endpoints from UI
- [ ] Response examples show

---

## 🖥️ ADMIN DASHBOARD SETUP

### Copy to XAMPP

```bash
cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
Copy-Item -Path "web_admin" -Destination "C:\xampp\htdocs\parking_admin" -Recurse
```

### Test Admin Dashboard

- [ ] Open `http://localhost/parking_admin/`
- [ ] Dashboard loads without errors
- [ ] "Active Vehicles: 0" shows (if no vehicles parked)
- [ ] Click "Refresh" button works
- [ ] Auto-refresh toggle can be enabled
- [ ] Table updates correctly

---

## 🔗 IoT INTEGRATION TEST

### Test Entry Gate Script

Save as `test_entry.py`:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/entry",
    json={"uid": "IOT_TEST_001"}
)
print(response.json())
```

Run:

```bash
python test_entry.py
```

- [ ] Response shows success=true
- [ ] transaction_id is assigned
- [ ] entry_time is recorded

---

### Test Exit Gate Script

Save as `test_exit.py`:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/exit",
    json={"uid": "IOT_TEST_001"}
)
data = response.json()
print(f"Fee: Rp {data['fee']:,.0f}")
print(f"Duration: {data['duration_minutes']} minutes")
```

Run:

```bash
python test_exit.py
```

- [ ] Response shows success=true
- [ ] Fee is calculated correctly
- [ ] Duration is correct
- [ ] Status changed to OUT

---

## 🐛 ERROR HANDLING TEST

### Test Invalid UID

```bash
curl -X POST http://localhost:8000/api/entry \
  -H "Content-Type: application/json" \
  -d '{"uid": ""}'
```

- [ ] Returns error
- [ ] Code = "INVALID_UID"
- [ ] Helpful error message

---

### Test Database Connection Error

1. Stop MySQL in XAMPP
2. Try: `curl http://localhost:8000/api/entry -d '{"uid": "TEST"}'`

- [ ] Returns error
- [ ] Code = "DATABASE_ERROR"
- [ ] Does not crash server

---

## 📊 DATABASE VERIFICATION

### Check All Tables

```bash
mysql -u root smart_parking_db << EOF
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='smart_parking_db';
SELECT COUNT(*) as entry_count FROM parking_transactions;
SELECT * FROM parking_rates;
EOF
```

Expected:

- [ ] 3 tables exist
- [ ] parking_transactions has records from tests
- [ ] parking_rates has 1 record (base_fee=5000, per_hour_fee=2000)

---

## 🌐 CORS & SECURITY TEST

### Test CORS Headers

```bash
curl -i -X OPTIONS http://localhost:8000/api/entry
```

- [ ] Response includes Access-Control headers
- [ ] Allows localhost origins

---

## 📝 DOCUMENTATION VERIFICATION

- [ ] README.md - Readable and complete
- [ ] SETUP_GUIDE.md - Clear step-by-step instructions
- [ ] PROJECT_SUMMARY.md - Overview provided
- [ ] API docs (Swagger) - All endpoints documented
- [ ] Code comments - Inline documentation present

---

## ✨ PRODUCTION READINESS

### Before Cloud Deployment

- [ ] Set DEBUG=False in .env
- [ ] Update DB credentials to cloud database
- [ ] Update CORS_ORIGINS to production URLs
- [ ] Test with production database
- [ ] Enable HTTPS (if required)
- [ ] Setup monitoring & logging
- [ ] Create backup strategy
- [ ] Document deployment steps

### Cloud Deployment (Railway Example)

- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Configure environment variables
- [ ] Set up MySQL database (Railway MySQL)
- [ ] Deploy and test endpoints
- [ ] Monitor logs and performance
- [ ] Setup auto-scaling (if needed)

---

## 📞 TROUBLESHOOTING LOG

Use this section to log any issues found:

| Issue                 | Solution           | Status |
| --------------------- | ------------------ | ------ |
| Database not found    | Import schema.sql  | ✅     |
| Cannot connect API    | Verify .env        | ✅     |
| Port 8000 in use      | Change API_PORT    | ✅     |
| Admin dashboard error | Check API_BASE_URL | ⏳     |
| IoT integration fail  | Verify network     | ⏳     |

---

## 🎉 FINAL VERIFICATION

All items checked?

- [ ] Database setup complete
- [ ] Python environment ready
- [ ] FastAPI server running
- [ ] All API endpoints tested
- [ ] Admin dashboard working
- [ ] IoT integration tested
- [ ] Error handling verified
- [ ] Documentation complete
- [ ] Ready for production

---

## 🚀 GO LIVE!

Once all checkboxes are checked:

1. ✅ Prepare production environment
2. ✅ Migrate to cloud database (optional)
3. ✅ Deploy to cloud platform
4. ✅ Setup monitoring & alerts
5. ✅ Integrate with all IoT devices
6. ✅ Go live!

---

## 📞 SUPPORT CONTACTS

- FastAPI Issues: https://github.com/tiangolo/fastapi/issues
- MySQL Issues: https://dev.mysql.com/doc/
- Python Issues: https://stackoverflow.com/questions/tagged/python

---

**Good luck with your Smart Parking IoT project! 🅿️**

Date: November 24, 2025
Version: 1.0.0
