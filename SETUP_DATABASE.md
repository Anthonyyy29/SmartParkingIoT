# 🗄️ Panduan Setup Database MySQL

## ✅ Step 1: Pastikan MySQL Sudah Running

### Opsi A: Menggunakan XAMPP (Windows)

1. Buka **XAMPP Control Panel**
2. Klik **Start** pada **Apache** dan **MySQL**
3. Tunggu hingga berwarna hijau ✅

### Opsi B: Menggunakan MySQL Langsung

```powershell
# Jika MySQL sudah terinstall, jalankan di terminal
net start MySQL80  # atau versi MySQL Anda
```

---

## ✅ Step 2: Buka MySQL Command Line atau MySQL Workbench

### Metode 1: MySQL Command Line (Termudah)

```powershell
# Buka PowerShell dan ketik:
mysql -u root -p

# Tekan Enter, akan diminta password (kosongkan saja, tekan Enter lagi)
```

### Metode 2: MySQL Workbench (GUI)

1. Buka **MySQL Workbench**
2. Double-click connection **Local instance MySQL80**
3. Masukkan password jika ada (biasanya kosong)

---

## ✅ Step 3: Import Database dari File SQL

### Metode 1: Command Line

```powershell
# Di PowerShell, pastikan sudah login MySQL:
mysql -u root -p smart_parking < C:\Kuliah\Semester\ 3\OOP-ProjectAkhir\SmartParkingIoT\setup_database.sql

# Atau ketik manual di MySQL:
source C:\Kuliah\Semester\ 3\OOP-ProjectAkhir\SmartParkingIoT\setup_database.sql;
```

**Catatan:** Gunakan `/` bukan `\` untuk path di MySQL:

```sql
source C:/Kuliah/Semester\ 3/OOP-ProjectAkhir/SmartParkingIoT/setup_database.sql;
```

### Metode 2: MySQL Workbench

1. Buka **File** → **Open SQL Script**
2. Pilih file `setup_database.sql`
3. Klik **Execute** (atau Ctrl+Shift+Enter)

---

## ✅ Step 4: Verifikasi Database Sudah Dibuat

```sql
-- Cek apakah database sudah ada
SHOW DATABASES;

-- Masuk ke database smart_parking
USE smart_parking;

-- Cek semua tabel
SHOW TABLES;

-- Lihat isi parking_rates (tarif)
SELECT * FROM parking_rates;
```

**Output yang diharapkan:**

```
+----+--------------+----------+-----------------+
| id | base_minutes | base_fee | per_minute_fee  |
+----+--------------+----------+-----------------+
|  1 |           60 |  5000.00 |          100.00 |
+----+--------------+----------+-----------------+
```

---

## ✅ Step 5: Jalankan Backend FastAPI

```powershell
# Pastikan sudah di folder project
cd C:\Kuliah\Semester\ 3\OOP-ProjectAkhir\SmartParkingIoT

# Jalankan aplikasi
python main.py
```

Jika sukses, akan muncul:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🔍 Troubleshooting

### Error: "Can't connect to MySQL server"

✅ **Solusi:** Pastikan MySQL sudah running di XAMPP

### Error: "Unknown database 'smart_parking'"

✅ **Solusi:** Jalankan script `setup_database.sql` terlebih dahulu

### Error: "Access denied for user 'root'@'localhost'"

✅ **Solusi:**

- Jika pakai XAMPP, biasanya user `root` tanpa password
- Ubah kredensial di `app/core/config.py` jika berbeda

```python
DATABASE_URL = "mysql+pymysql://root:PASSWORD@localhost/smart_parking"
# Ganti PASSWORD dengan password MySQL Anda
```

---

## 📝 Ringkas Struktur Database

| Tabel                  | Fungsi                           |
| ---------------------- | -------------------------------- |
| `parking_rates`        | Menyimpan tarif parkir           |
| `vehicles`             | Menyimpan data kendaraan         |
| `parking_transactions` | Menyimpan transaksi masuk/keluar |

---

## ✨ Selesai!

Sekarang database sudah siap dan backend dapat berjalan dengan baik! 🎉
