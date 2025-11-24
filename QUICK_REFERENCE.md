#!/usr/bin/env python
"""
Quick Reference - Smart Parking IoT API
Handy reference untuk command dan endpoint yang sering digunakan
"""

# ============================================================================

# 🚀 STARTUP COMMANDS

# ============================================================================

"""

1. Start XAMPP MySQL

   - Open XAMPP Control Panel
   - Click Start on MySQL

2. Install Dependencies
   cd "c:\Kuliah\Semester 3\OOP-ProjectAkhir\SmartParkingIoT"
   pip install -r requirements.txt

3. Run FastAPI Server
   python main.py
   Expected: ✅ Connected to smart_parking_db database
   INFO: Uvicorn running on http://0.0.0.0:8000
   """

# ============================================================================

# 📡 API ENDPOINTS - QUICK REFERENCE

# ============================================================================

# Health Check

# GET http://localhost:8000/health

# Response: { "status": "healthy", "database": "connected" }

# Vehicle Entry

# POST http://localhost:8000/api/entry

# Body: { "uid": "RFID001" }

# Response: { "success": true, "transaction_id": 1, "entry_time": "..." }

# Vehicle Exit

# POST http://localhost:8000/api/exit

# Body: { "uid": "RFID001" }

# Response: { "success": true, "fee": 5000, "duration_minutes": 45, ... }

# Get Parking Status

# GET http://localhost:8000/api/parking-status

# Response: { "success": true, "active_vehicles": 2, "vehicles": [...] }

# Get Last Transaction

# GET http://localhost:8000/api/last-transaction/RFID001

# Response: { "success": true, "uid": "RFID001", "status": "OUT", ... }

# ============================================================================

# 🧪 QUICK CURL TESTS

# ============================================================================

"""

# Test Health

curl http://localhost:8000/health

# Test Entry

curl -X POST http://localhost:8000/api/entry \
 -H "Content-Type: application/json" \
 -d '{"uid": "TEST001"}'

# Test Exit

curl -X POST http://localhost:8000/api/exit \
 -H "Content-Type: application/json" \
 -d '{"uid": "TEST001"}'

# Get Status

curl http://localhost:8000/api/parking-status

# Query Last Transaction

curl http://localhost:8000/api/last-transaction/TEST001
"""

# ============================================================================

# 🔧 COMMON CONFIGURATION

# ============================================================================

"""
.env File Defaults:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=smart_parking_db
API_PORT=8000
DEBUG=True

For Production:
DEBUG=False
DB_HOST=cloud-db-host
DB_PASSWORD=secure_password
"""

# ============================================================================

# 📊 PRICING QUICK REFERENCE

# ============================================================================

"""
First 60 minutes: Rp 5.000
Each hour after: +Rp 2.000

Examples:
45 min = Rp 5.000
60 min = Rp 5.000
75 min = Rp 7.000
120 min = Rp 7.000
150 min = Rp 9.000
"""

# ============================================================================

# 🔗 PYTHON CLIENT QUICK START

# ============================================================================

"""
import requests

# Entry

response = requests.post(
"http://localhost:8000/api/entry",
json={"uid": "RFID001"}
)
print(response.json())

# Exit

response = requests.post(
"http://localhost:8000/api/exit",
json={"uid": "RFID001"}
)
data = response.json()
print(f"Fee: Rp {data['fee']:,.0f}")
print(f"Duration: {data['duration_minutes']} minutes")
"""

# ============================================================================

# 📁 IMPORTANT FILES

# ============================================================================

"""
Main Entry Point:

- main.py ← RUN THIS

Configuration:

- .env ← Customize here
- config.py ← Settings

Database:

- database/schema.sql ← Import to MySQL

API Routes:

- routes/entry.py ← POST /api/entry
- routes/exit.py ← POST /api/exit
- routes/admin.py ← GET /api/parking-status

Admin Dashboard:

- web_admin/index.html ← Copy to htdocs

Documentation:

- README.md
- SETUP_GUIDE.md
- PROJECT_SUMMARY.md
- DEPLOYMENT_CHECKLIST.md
  """

# ============================================================================

# 🖥️ WEB INTERFACES

# ============================================================================

"""
API Documentation:
http://localhost:8000/docs

API ReDoc:
http://localhost:8000/redoc

Admin Dashboard:
http://localhost/parking_admin/

phpMyAdmin:
http://localhost/phpmyadmin/
"""

# ============================================================================

# 🐛 TROUBLESHOOTING QUICK FIXES

# ============================================================================

"""
Database Error:
mysql -u root smart_parking_db < database/schema.sql

Port in use:
Change API_PORT in .env
Or: netstat -ano | findstr :8000 (then kill process)

Connection refused:

1. Check XAMPP MySQL is running
2. Check .env DB_HOST and port

Admin dashboard not updating:
Check API_BASE_URL in web_admin/script.js
"""

# ============================================================================

# 📋 DEPLOYMENT STEPS

# ============================================================================

"""

1. Setup Database

   - Create database: smart_parking_db
   - Import: database/schema.sql

2. Install Dependencies
   pip install -r requirements.txt

3. Configure Environment

   - Update .env with your settings

4. Run Server
   python main.py

5. Setup Admin Dashboard
   Copy web_admin/ to C:\xampp\htdocs\parking_admin

6. Integrate IoT
   Import client code from iot_client_example.py

7. Test Everything
   Follow DEPLOYMENT_CHECKLIST.md

8. Deploy to Cloud (Optional)
   - Update .env for production
   - Deploy to Railway/Render
   - Setup cloud database
     """

# ============================================================================

# 🚀 CLOUD DEPLOYMENT QUICK REFERENCE

# ============================================================================

"""
Railway Deployment:

1. railway login
2. railway init
3. railway up
4. Configure env vars in Railway dashboard
5. Connect Railway MySQL database

Procfile (create if needed):
web: uvicorn main:app --host 0.0.0.0 --port $PORT
"""

# ============================================================================

# 📞 QUICK LINKS

# ============================================================================

"""
FastAPI Docs: https://fastapi.tiangolo.com
MySQL Docs: https://dev.mysql.com/doc/
Python Requests: https://requests.readthedocs.io
Railway: https://railway.app
Render: https://render.com
"""

# ============================================================================

# ✨ SUMMARY

# ============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ Smart Parking IoT - Quick Reference ║
╠════════════════════════════════════════════════════════════════════════════╣
║ ║
║ 🚀 STARTUP: ║
║ 1. Start XAMPP MySQL ║
║ 2. python main.py ║
║ ║
║ 📡 TEST API: ║
║ • http://localhost:8000/docs (Swagger UI) ║
║ • curl http://localhost:8000/health ║
║ ║
║ 🖥️ ADMIN: ║
║ • http://localhost/parking_admin/ ║
║ ║
║ 📚 DOCS: ║
║ • README.md - Full documentation ║
║ • SETUP_GUIDE.md - Step-by-step ║
║ • DEPLOYMENT_CHECKLIST.md - Testing ║
║ ║
║ 💰 PRICING: ║
║ • 60 min: Rp 5.000 ║
║ • Each hour after: +Rp 2.000 ║
║ ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

# Remember: Keep this file for quick reference!

# Last Updated: November 24, 2025
