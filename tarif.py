from datetime import datetime
import math


def hitungWaktuMasuk():
    """Kembalikan objek datetime saat ini (waktu masuk)."""
    return datetime.now()


def hitungWaktuKeluar():
    """Kembalikan objek datetime saat ini (waktu keluar)."""
    return datetime.now()


def format_waktu(dt: datetime) -> str:
    """Format datetime menjadi string yang mudah dibaca."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def hitung_durasi(masuk: datetime, keluar: datetime):
    """Mengembalikan tuple (durasi_menit, jam_terhitung).

    jam_terhitung adalah pembulatan ke atas per jam (ceil).
    """
    if keluar < masuk:
        raise ValueError("Waktu keluar harus setelah waktu masuk")
    total_seconds = (keluar - masuk).total_seconds()
    durasi_menit = total_seconds / 60
    jam_terhitung = math.ceil(durasi_menit / 60) if durasi_menit > 0 else 0
    return durasi_menit, jam_terhitung


def pilihKendaraan():
    """Menampilkan pilihan kendaraan dan mengembalikan string jenisnya."""
    while True:
        print("Jenis Kendaraan :")
        print("1. Motor")
        print("2. Mobil")
        print("3. Kendaraan Besar")
        pil = input("Jawaban anda (1/2/3): ").strip()
        if pil == "1":
            return "Motor"
        elif pil == "2":
            return "Mobil"
        elif pil == "3":
            return "Kendaraan Besar"
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")


def tarifParkir(kendaraan: str) -> int:
    """Kembalikan tarif per jam sesuai jenis kendaraan."""
    if kendaraan == "Motor":
        return 2000
    elif kendaraan == "Mobil":
        return 5000
    elif kendaraan == "Kendaraan Besar":
        return 10000
    else:
        raise ValueError("Jenis kendaraan tidak dikenali")


def main_loop():
    print("=== Parkir Juwita ===")
    while True:
        # Tanyakan apakah ingin mulai parkir
        ans = input("Apakah anda ingin masuk? (y/n): ").strip().lower()
        if ans == "n":
            print("Terima kasih. Program selesai.")
            break
        if ans != "y":
            print("Input tidak dikenali. Masukkan 'y' atau 'n'.")
            continue

        # Mulai sesi parkir
        waktu_masuk = hitungWaktuMasuk()
        print("Waktu masuk tercatat:", format_waktu(waktu_masuk))

        # Pilih kendaraan dan tarif
        kendaraan = pilihKendaraan()
        tarif = tarifParkir(kendaraan)
        print(f"Kendaraan: {kendaraan} | Tarif per jam: Rp{tarif}")

        # Tunggu sampai keluar
        while True:
            ans_out = input("Apakah kendaraan keluar sekarang? (y untuk keluar, t untuk batal): ").strip().lower()
            if ans_out == "t":
                print("Sesi dibatalkan. Kembali ke menu utama.")
                break
            if ans_out != "y":
                print("Masukkan 'y' untuk keluar atau 't' untuk batal.")
                continue

            waktu_keluar = hitungWaktuKeluar()
            print("Waktu keluar tercatat:", format_waktu(waktu_keluar))

            durasi_menit, jam_terhitung = hitung_durasi(waktu_masuk, waktu_keluar)
            total = jam_terhitung * tarif

            print("--- Ringkasan ---")
            print("Masuk :", format_waktu(waktu_masuk))
            print("Keluar:", format_waktu(waktu_keluar))
            print(f"Durasi (menit): {durasi_menit:.1f}")
            print(f"Jam yang dihitung: {jam_terhitung} jam")
            print(f"Total tarif: Rp{total}")
            print("-----------------")
            break


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")


    






