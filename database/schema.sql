-- Smart Parking IoT Database Schema
-- Database: smart_parking_db

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE IF NOT EXISTS `vehicles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(50) NOT NULL COMMENT 'RFID UID kendaraan',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `idx_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parking_rates`
--

CREATE TABLE IF NOT EXISTS `parking_rates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_minutes` int(11) NOT NULL COMMENT 'Durasi dasar dalam menit',
  `base_fee` decimal(10,2) NOT NULL COMMENT 'Biaya dasar dalam Rupiah',
  `per_hour_fee` decimal(10,2) NOT NULL COMMENT 'Biaya per jam tambahan',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parking_rates`
--

INSERT INTO `parking_rates` (`id`, `base_minutes`, `base_fee`, `per_hour_fee`, `created_at`) VALUES
(1, 60, 5000.00, 2000.00, current_timestamp());

-- --------------------------------------------------------

--
-- Table structure for table `parking_transactions`
--

CREATE TABLE IF NOT EXISTS `parking_transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(50) NOT NULL COMMENT 'RFID UID kendaraan',
  `entry_time` datetime NOT NULL COMMENT 'Waktu masuk',
  `exit_time` datetime DEFAULT NULL COMMENT 'Waktu keluar',
  `duration_minutes` int(11) DEFAULT NULL COMMENT 'Durasi parkir dalam menit',
  `fee` decimal(10,2) DEFAULT NULL COMMENT 'Biaya dalam Rupiah',
  `status` enum('IN','OUT') DEFAULT 'IN' COMMENT 'Status transaksi',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`),
  KEY `idx_entry_time` (`entry_time`),
  KEY `idx_status` (`status`),
  CONSTRAINT `parking_transactions_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `vehicles` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
