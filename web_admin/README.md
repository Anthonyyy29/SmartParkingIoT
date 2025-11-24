# Web Admin Dashboard

Dashboard untuk monitoring real-time kendaraan yang sedang parkir.

## Fitur

- ✅ Real-time monitoring kendaraan yang sedang parkir
- ✅ Tampil durasi parkir dan biaya per kendaraan
- ✅ Auto-refresh data setiap 5 detik
- ✅ Responsive design (mobile-friendly)
- ✅ Tampil total revenue harian

## Setup

### Option 1: Dari XAMPP (Recommended untuk Local Development)

1. Copy folder `web_admin` ke `C:\xampp\htdocs\`

   ```bash
   xcopy web_admin C:\xampp\htdocs\parking_admin\ /E /I
   ```

2. Buka browser: `http://localhost/parking_admin/`

### Option 2: Langsung buka file HTML

1. Buka file `index.html` dengan double-click
2. Atau buka dengan browser: `File > Open > index.html`

### Option 3: Dari FastAPI (Serve as Static Files)

Tambahkan kode ini di `main.py`:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/admin", StaticFiles(directory="web_admin", html=True), name="admin")
```

Kemudian buka: `http://localhost:8000/admin/`

## Konfigurasi

Edit file `script.js` untuk mengubah:

```javascript
// API Base URL
const API_BASE_URL = "http://localhost:8000"; // Production: https://api.example.com

// Auto refresh interval (ms)
const REFRESH_INTERVAL = 5000; // 5 seconds
```

## API Integration

Dashboard ini menggunakan 2 endpoint dari FastAPI:

### GET /api/parking-status

Dapatkan list kendaraan yang sedang parkir

Response:

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
    }
  ]
}
```

### Browser DevTools

Buka Console (F12) untuk melihat:

- Log real-time
- Error messages
- Debugging info

## Troubleshooting

### Dashboard tidak bisa connect ke API

- Pastikan FastAPI server berjalan (`python main.py`)
- Check URL di `script.js` sesuai dengan server
- Check CORS configuration di `main.py`

### Data tidak update

- Klik tombol "Refresh" manual
- Atau enable "Auto Refresh"
- Check browser console (F12) untuk error

### Hanya bisa buka dari lokal, tidak dari IP lain

- Update `API_BASE_URL` di `script.js` dengan IP server
- Pastikan firewall allow port 8000

## File Structure

```
web_admin/
├── index.html      # HTML template
├── style.css       # Styling
├── script.js       # JavaScript logic
└── README.md       # This file
```
