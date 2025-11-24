-- ============================================
-- SMART PARKING IoT - Database Setup
-- ============================================
-- Jalankan script ini di MySQL untuk setup database

-- 1. Buat Database
CREATE DATABASE IF NOT EXISTS smart_parking;
USE smart_parking;

-- 2. Tabel Parking Rates (Tarif Parkir)
CREATE TABLE IF NOT EXISTS parking_rates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    base_minutes INT NOT NULL COMMENT 'Durasi dasar dalam menit',
    base_fee DECIMAL(10,2) NOT NULL COMMENT 'Biaya dasar dalam Rupiah',
    per_minute_fee DECIMAL(10,2) NOT NULL COMMENT 'Biaya per menit tambahan',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created (created_at)
);

-- 3. Tabel Vehicles (Kendaraan)
CREATE TABLE IF NOT EXISTS vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate VARCHAR(50) UNIQUE NOT NULL COMMENT 'Plat nomor kendaraan',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_plate (plate)
);

-- 4. Tabel Parking Transactions (Transaksi Parkir)
CREATE TABLE IF NOT EXISTS parking_transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plate VARCHAR(50) NOT NULL COMMENT 'Plat nomor kendaraan',
    entry_time DATETIME NOT NULL COMMENT 'Waktu masuk',
    exit_time DATETIME NULL COMMENT 'Waktu keluar',
    duration_minutes INT NULL COMMENT 'Durasi parkir dalam menit',
    fee DECIMAL(10,2) NULL COMMENT 'Biaya dalam Rupiah',
    status ENUM('IN', 'OUT', 'PAID', 'DONE') DEFAULT 'IN' COMMENT 'Status transaksi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_plate (plate),
    INDEX idx_entry_time (entry_time),
    INDEX idx_status (status),
    FOREIGN KEY (plate) REFERENCES vehicles(plate) ON DELETE CASCADE
);

-- 5. Insert Tarif Default
-- Tarif: 60 menit pertama = Rp5.000, setiap menit tambahan = Rp100
INSERT INTO parking_rates (base_minutes, base_fee, per_minute_fee) 
VALUES (60, 5000, 100);

-- ============================================
-- SELESAI! Database sudah siap digunakan
-- ============================================
